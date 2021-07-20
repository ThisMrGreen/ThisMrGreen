
client = TelegramClient(phone, api_id, api_hash)
client.start()


@dp.callback_query_handler(lambda call: call.data == 'start_client')
async def process_callback(call: types.CallbackQuery, state: FSMContext):
    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request(user_phone_input)
        await call.message.answer("Введите код подтверждения:")
        await InviteAttributes.user_code.set()
    else:
        await call.message.answer(f"Клиент {user_session_name_input} стартовал!",
                                  reply_markup=keyboards.start_script_markup)
        # await InviteAttributes.start_script.set()
        await state.finish()


@dp.message_handler(state=InviteAttributes.user_code)
async def user_code_result(message: types.Message, state: FSMContext):
    user_code_input = message.text
    await state.update_data(user_code_input=user_code_input)
    await client.sign_in(user_phone_input, user_code_input)
    await message.answer(f"Аккаунт {user_session_name_input} успешно подключен!",
                         reply_markup=keyboards.start_script_markup)
    # await InviteAttributes.start_script.set()
    await state.finish()
    
    
    # ПРИМЕР ДАЛЬНЕЙШЕГО ИСПОЛЬЗОВАНИЯ КЛИЕНТА
    
@dp.callback_query_handler(lambda call: call.data == 'start_script')
async def process_callback(call: types.CallbackQuery, state: FSMContext):

    chats = []
    last_date = None
    chunk_size = 200
    groups = []

    result = await client(GetDialogsRequest(
        offset_date=last_date,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=chunk_size,
        hash=0
    ))
    chats.extend(result.chats)

    for chat in chats:
        try:
            if chat.megagroup == True:
                groups.append(chat)
        except:
            continue

    i = 0
    for group in groups:
        await message.answer(str(i) + ' - ' + group.title)
        i += 1
        
        
