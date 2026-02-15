import telegram
from telegram.ext import ContextTypes

import core


async def delete(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if len(context.args) == 0:
            await update.message.reply_text("Usage:\n/delete ID1 ID2 ID3 ...")
            return
        
        sheet = core.get_sheet()
        ids = sheet.col_values(1)
        
        rows_to_delete = []
        deleted_ids = []
        failed_ids = []
        
        # Collect all rows to delete
        for target_id_str in context.args:
            try:
                target_id = int(target_id_str)
                row = ids.index(str(target_id)) + 1
                rows_to_delete.append(row)
                deleted_ids.append(target_id)
            except ValueError:
                failed_ids.append(target_id_str)
        
        # Delete rows in reverse order (from bottom to top) to avoid row number shifts
        for row in sorted(rows_to_delete, reverse=True):
            sheet.delete_rows(row)
        
        message = ""
        if deleted_ids:
            message += f"Deleted IDs: {', '.join(map(str, deleted_ids))}"
        if failed_ids:
            if message:
                message += "\n"
            message += f"Failed to delete: {', '.join(failed_ids)}"
        
        await update.message.reply_text(message if message else "No IDs deleted")
    except Exception as e:
        await update.message.reply_text("Usage:\n/delete ID1 ID2 ID3 ...")
