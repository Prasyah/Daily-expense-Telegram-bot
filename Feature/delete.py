import telegram
from telegram.ext import ContextTypes

import core


async def delete(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if len(context.args) == 0:
            await update.message.reply_text("Usage:\n/delete ID1 ID2 ID3 ...\n\nNote: /delete is for EXPENSES only.\nUse /reimburse delete for reimbursements.")
            return
        
        sheet = core.get_sheet()
        ids = sheet.col_values(1)
        
        rows_to_delete = []
        deleted_ids = []
        failed_ids = []
        
        # Collect all rows to clear from expense table (column A-F)
        for target_id_str in context.args:
            try:
                target_id = int(target_id_str)
                row = ids.index(str(target_id)) + 1
                rows_to_delete.append(row)
                deleted_ids.append(target_id)
            except ValueError:
                failed_ids.append(target_id_str)
        
        # Clear cells in reverse order to avoid confusion
        for row in sorted(rows_to_delete, reverse=True):
            sheet.update(f"A{row}:F{row}", [["", "", "", "", "", ""]])
        
        message = ""
        if deleted_ids:
            message += f"Deleted expense IDs: {', '.join(map(str, deleted_ids))}"
        if failed_ids:
            if message:
                message += "\n"
            message += f"Failed to delete: {', '.join(failed_ids)}\n(Only delete expense entries with /delete)\nUse /reimburse delete for reimbursements."
        
        await update.message.reply_text(message if message else "No IDs deleted")
    except Exception as e:
        await update.message.reply_text("Usage:\n/delete ID1 ID2 ID3 ...\n\nNote: /delete is for EXPENSES only.\nUse /reimburse delete for reimbursements.")
