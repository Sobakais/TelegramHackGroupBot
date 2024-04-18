from aiogram import Router, F
from aiogram.types import Message
from aiogram.types import FSInputFile, URLInputFile, BufferedInputFile

router = Router()


@router.message(F.voice)
async def voice_handler(message: Message):
    voice_from_url = URLInputFile(
        "https://nkprod-coredatastack-pa7jx42xiwhf-tasksbucket-13qb6gn1l5ooi.s3.us-east-1.amazonaws.com/d5e3c8f6-bd70-4010-a8dc-07d0979b6ed0/result.wav?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAUENQVYXORYD4N3EU%2F20240418%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240418T165427Z&X-Amz-Expires=86400&X-Amz-Signature=930775a3ba44e2c5f1f13a725a27dc8514f44b12615195e19a46c0e074e5d4c9&X-Amz-SignedHeaders=host&response-content-disposition=attachment%3B%20filename%3D%22%25D0%25BA%25D1%2583%25D0%25BA%25D0%25B0%2520%25D0%25B8%2520%25D0%25BF%25D1%2583%25D0%25BA%25D0%25B0%2520%25D0%25BB%25D1%258E%25D0%25B1%25D0%25B8%25D0%25BB%25D0%25B8%2520%25D0%25B5.wav%22&x-id=GetObject"
    )
    await message.answer_voice(voice=voice_from_url)


@router.message(F.video_note)
async def circles_handler(message: Message):
    await message.answer("Circles message")
