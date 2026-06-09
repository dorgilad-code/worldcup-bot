from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import asyncio
from bot import send_daily_tips

async def main():
    scheduler = AsyncIOScheduler(timezone="Asia/Jerusalem")
    
    scheduler.add_job(
        send_daily_tips,
        CronTrigger(hour=8, minute=0),
        id="daily_tips"
    )
    
    scheduler.start()
    print("🤖 הבוט פעיל! שולח טיפים כל בוקר ב-08:00")
    
    await send_daily_tips()
    
    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        scheduler.shutdown()

if __name__ == "__main__":
    asyncio.run(main())