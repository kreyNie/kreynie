from vkbottle.user import Message, UserLabeler

from .rules import Rights, CheckRights, check_permissions


help_labeler = UserLabeler()
help_labeler.vbml_ignore_case = True
help_labeler.custom_rules["access"] = CheckRights


@help_labeler.private_message(access=Rights.moderator, text="помощь")
async def help_handler(message: Message):
    raw_help = [
        "Использование бота:",
        "▶️ Бан <userID> <comment> <time>",
        "• <userID> - ссылка на страницу",
        '• <comment> - "ключ" для комментария бана. Для уточнения введи команду "Сокращения"',
        "• <time> - срок бана",
        "---> Бан https://vk.com/steel_wg оффтоп день",
        "⚠️ Для банов от недели и выше требуются скриншоты для публикации в баню",
        "▶️ Сокращения - для просмотра всех доступных сокращений",
    ]
    user_id = str(message.from_id)
    current_permissions = await check_permissions(user_id, 2)
    if current_permissions:
        raw_help.extend(
            (
                "\n\n",
                "Закрытые модераторские команды: ",
                "▶️ Рассылка <text> - рассылает <text> в исходном виде всем модератором из списка бота",
                "▶️ Добмод <vkID> <MBid>, где <vkID> - ссылка на страницу, <MBid> - НОМЕР модератора",
                "--> Пример: Добмод vk.com/steel_wg 69",
                "▶️ Удалмод <vkID>, где <vkID> - ссылка на страницу",
                "▶️ Модсписок",
            )
        )

    current_permissions = await check_permissions(user_id, 3)
    if current_permissions:
        raw_help.extend(
            (
                "\n\n",
                "Команды для лидов: ",
                "▶️ Минус <text> - используется вместе с репостом неправильного бана из Бани в ЛС боту. Текст отправляется модератору в ЛС",
            )
        )

    current_permissions = await check_permissions(user_id, 4)
    if current_permissions:
        raw_help.extend(
            (
                "\n\n",
                "Остальные команды: ",
                "▶️ Права <user_id> <rights:int>",
                "ai_active",
                "ai_disable",
                "ai_add_text <level> <text>",
            )
        )

    await message.answer("\n".join(raw_help))


@help_labeler.private_message(access=Rights.moderator, text="Сокращения")
async def getAbbreviations(message: Message):
    await message.answer(
        message="Доступные сокращения",
        attachment="photo776084434_457239060",
    )
