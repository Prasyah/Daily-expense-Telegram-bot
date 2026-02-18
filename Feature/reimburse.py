import telegram
from telegram.ext import ContextTypes
import pytz
from datetime import datetime

import core


def _parse_int(value):
    try:
        return int(value)
    except Exception:
        try:
            # remove non-digits
            cleaned = "".join(c for c in str(value) if c.isdigit())
            return int(cleaned) if cleaned else 0
        except Exception:
            return 0


async def reimburse(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    sheet = core.get_sheet()
    now = datetime.now(pytz.timezone(core.TIMEZONE))

    # Subcommands: edit, delete, detail
    if len(context.args) >= 1 and context.args[0].lower() == "detail":
        # Read reimburse budget block H17:K23 and transactions O2:T
        try:
            budget_rows = sheet.get("H17:K23") or []
            if not budget_rows:
                await update.message.reply_text("No reimburse budget data")
                return

            text = "📋 Reimburse Budgets and Expenses\n\n"
            for r in budget_rows[:-1]:
                # r: [Category, Budget, Expense, Leftover]
                cat = r[0] if len(r) > 0 else ""
                bud = _parse_int(r[1]) if len(r) > 1 else 0
                exp = _parse_int(r[2]) if len(r) > 2 else 0
                left = _parse_int(r[3]) if len(r) > 3 else bud - exp
                text += f"{cat}: Budget Rp{bud:,} | Expense Rp{exp:,} | Left Rp{left:,}\n"

            # last row is totals (if present)
            if len(budget_rows) >= 1:
                total_row = budget_rows[-1]
                if len(total_row) >= 3:
                    try:
                        total_budget = _parse_int(total_row[1])
                        total_exp = _parse_int(total_row[2])
                        text += f"\nTotal Budget: Rp{total_budget:,} | Total Expense: Rp{total_exp:,}"
                    except Exception:
                        pass

            # Fetch all reimburse transactions
            trans_data = sheet.get("O2:T1000") or []
            if trans_data:
                text += "\n\n🧾 All Reimbursement Transactions\n\n"
                for row in trans_data:
                    if len(row) >= 6:
                        trans_id = row[0]
                        trans_date = row[1]
                        trans_time = row[2]
                        trans_cat = row[3]
                        trans_amt = row[4]
                        trans_desc = row[5]
                        
                        # Skip empty rows
                        if not trans_id or trans_id == "":
                            continue
                        
                        amt_val = _parse_int(trans_amt)
                        text += f"ID {trans_id} | {trans_time} ({trans_date})\n"
                        text += f"• {trans_cat}: Rp{amt_val:,}\n"
                        text += f"  {trans_desc}\n\n"

            await update.message.reply_text(text)
        except Exception as e:
            await update.message.reply_text(f"Failed to read reimburse detail: {str(e)}")

        return

    if len(context.args) >= 1 and context.args[0].lower() == "edit":
        # /reimburse edit ID category description amount date(optional)
        try:
            target_id = int(context.args[1])
            category = context.args[2]
            
            last_arg = context.args[-1]
            
            if last_arg.isdigit() and 1 <= int(last_arg) <= 31:
                day = int(last_arg)
                amount = int(context.args[-2])
                description = " ".join(context.args[3:-2])
            else:
                amount = int(context.args[-1])
                description = " ".join(context.args[3:-1])
                day = None

            ids = sheet.col_values(15)
            row = ids.index(str(target_id)) + 1

            # Category -> column R (18), Amount -> S (19), Description -> T (20)
            sheet.update(f"R{row}", [[category]])
            sheet.update(f"S{row}", [[amount]])
            sheet.update(f"T{row}", [[description]])
            
            if day is not None:
                date_obj = now.replace(day=day)
                date = date_obj.strftime("%Y-%m-%d")
                sheet.update(f"P{row}", [[date]])

            await update.message.reply_text(f"Reimburse ID {target_id} updated")
        except Exception:
            await update.message.reply_text("Usage:\n/reimburse edit ID category description amount date(optional)")

        return

    if len(context.args) >= 1 and context.args[0].lower() == "delete":
        # /reimburse delete ID1 ID2 ... (clear cells for reimburse entries only)
        try:
            if len(context.args) == 1:
                await update.message.reply_text("Usage:\n/reimburse delete ID1 ID2 ...\n\nNote: /reimburse delete is for REIMBURSEMENTS only.\nUse /delete for expenses.")
                return

            ids = sheet.col_values(15)
            deleted = []
            failed = []
            for target_id_str in context.args[1:]:
                try:
                    tid = int(target_id_str)
                    row = ids.index(str(tid)) + 1
                    # Clear O..T cells on that row
                    sheet.update(f"O{row}:T{row}", [["", "", "", "", "", ""]])
                    deleted.append(tid)
                except Exception:
                    failed.append(target_id_str)

            msg = ""
            if deleted:
                msg += f"Cleared reimburse IDs: {', '.join(map(str, deleted))}"
            if failed:
                if msg:
                    msg += "\n"
                msg += f"Failed: {', '.join(failed)}\n(Only delete reimbursement entries with /reimburse delete)\nUse /delete for expenses."

            await update.message.reply_text(msg if msg else "No IDs cleared")
        except Exception:
            await update.message.reply_text("Usage:\n/reimburse delete ID1 ID2 ...\n\nNote: /reimburse delete is for REIMBURSEMENTS only.\nUse /delete for expenses.")

        return

    # Default: create new reimburse entry
    try:
        if len(context.args) == 0:
            await update.message.reply_text(
                "Usage:\n/reimburse reimburse_category description amount date(optional)"
            )
            return

        category = context.args[0]
        if category not in core.REIMBURSE_CATEGORIES:
            await update.message.reply_text("Invalid reimburse category")
            return

        last_arg = context.args[-1]
        if last_arg.isdigit() and 1 <= int(last_arg) <= 31:
            day = int(last_arg)
            amount = int(context.args[-2])
            description = " ".join(context.args[1:-2])
        else:
            day = now.day
            amount = int(context.args[-1])
            description = " ".join(context.args[1:-1])

        date_obj = now.replace(day=day)
        date = date_obj.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")

        no_list = sheet.col_values(15)
        if len(no_list) <= 1:
            next_no = 1
        else:
            next_no = int(no_list[-1]) + 1

        next_row = len(no_list) + 1

        sheet.update(
            f"O{next_row}:T{next_row}",
            [[
                next_no,
                date,
                time,
                category,
                amount,
                description
            ]],
            value_input_option="USER_ENTERED"
        )

        await update.message.reply_text(f"Reimburse saved with ID {next_no}")
    except Exception:
        await update.message.reply_text(
            "Usage:\n"
            "/reimburse reimburse_category description amount date(optional)\n"
            "Categories: Telkom, SF, Sat, XL, Tri, Other\n"
        )
