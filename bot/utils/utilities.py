from bot.utils.models import Product
from loguru import logger


def help_message() -> str:
    return (
        "<b>КАК ПОЛЬЗОВАТЬСЯ БОТОМ?</b>\n\n"
        "<u>Основные команды</u>\n"
        "/start - вызов главного меню;\n"
        "/list - список позиций;\n"
        "/truncate - удалить все позиции;\n\n"
        "<u>Добавление товаров для отслеживания</u>\n"
        "Отправить боту артикул или ссылку товара с Wildberries.\n\n"
        "<u>Удаление товаров</u>\n"
        "<b>Удалить по одному:</b> нажать на кнопку и отправить артикул.\n"
        "<b>Удалить все сразу:</b> нажать на кнопку и подтвердить удаление."
    )


async def generate_page_product(products: list[Product]) -> str:
    message: str = "<u>📋 Список товаров</u>:\n\n"
    for product in products:
        if product.count != 0:
            line = (
                f"▫️ <b>{product.brand} {product.name} {product.colors}</b>\n"
                f"<b>Цена:</b> {product.price} руб. "
                f"<b>Количество:</b> {product.count} шт. "
                f"<b>Артикул:</b> <code>{product.article}</code>\n"
                f"<a href='https://www.wildberries.ru/catalog/{product.article}/detail.aspx'>СТРАНИЦА ТОВАРА</a>\n\n"
            )
            message += line
        else:
            line = (
                f"▫️ <b>{product.brand} {product.name} {product.colors}</b>\n"
                f"<b>Артикул:</b> <code>{product.article}</code> "
                f"<b>Нет в наличии</b>\n"
                f"<a href='https://www.wildberries.ru/catalog/{product.article}/detail.aspx'>СТРАНИЦА ТОВАРА</a>\n\n"
            )
            message += line
    return message


def wb_create_product_message(product: Product) -> str:
    # TODO сделать обработку списка list[Product]
    if product.count == 0:
        # Товара нет в наличии на сайте
        return (
            f"✅ Позиция добавлена:\n"
            f"<b>{product.brand} {product.name} {product.colors}</b>\n"
            f"<b>Продавец</b> <a href='https://www.wildberries.ru/seller/{product.supplier_id}'>{product.supplier}</a>\n"
            f"<b>Артикул:</b> <code>{product.article}</code>\n\n"
            f"Сейчас товара нет в наличии.\n"
            f"Вам <b>придет уведомление</b>, когда он <b>появился на сайте</b>."
        )
    else:
        # Товар в наличии на сайте
        return (
            f"✅  Позиция добавлена:\n"
            f"<b>{product.brand} {product.name} {product.colors}</b>\n"
            f"<b>Цена:</b> {product.price} руб.\n"
            f"<b>Количество:</b> {product.count} шт.\n"
            f"<b>Продавец</b> "
            f"<a href='https://www.wildberries.ru/seller/{product.supplier_id}'>{product.supplier}</a>\n"
            f"<b>Артикул:</b> <code>{product.article}</code>\n\n"
        )


def wb_alert_user_about_lowed_price(old_product: Product, new_product: Product) -> str:
    logger.info(
        f"Цена снизилась {new_product.article} с {old_product.price} на {new_product.price}"
    )
    return (
        f"<b>Цена снижена</b>\n"
        f"<b>{new_product.brand} {new_product.name} {new_product.colors}</b> "
        f"<b>Цена:</b> {old_product.price} / {new_product.price} руб. "
        f"<b>Количество:</b> {new_product.count} шт. "
        f"<b>Артикул:</b> <code>{new_product.article}</code> "
        f"<b>Продавец:</b> "
        f"<a href='https://www.wildberries.ru/seller/{new_product.supplier_id}'>{new_product.supplier}</a>\n"
        f"<a href='https://www.wildberries.ru/catalog/{new_product.article}/detail.aspx'>СТРАНИЦА ТОВАРА</a>"
    )


def wb_alert_user_about_upped_price(old_product: Product, new_product: Product) -> str:
    logger.info(
        f"Цена возросла {new_product.article} с {old_product.price} на {new_product.price}"
    )
    return (
        f"<b>Цена возросла</b>\n"
        f"<b>{new_product.brand} {new_product.name} {new_product.colors}</b> "
        f"<b>Цена:</b> {old_product.price} / {new_product.price} руб. "
        f"<b>Количество:</b> {new_product.count} шт. "
        f"<b>Артикул:</b> <code>{new_product.article}</code> "
        f"<b>Продавец:</b> "
        f"<a href='https://www.wildberries.ru/seller/{new_product.supplier_id}'>{new_product.supplier}</a>\n"
        f"<a href='https://www.wildberries.ru/catalog/{new_product.article}/detail.aspx'>СТРАНИЦА ТОВАРА</a>"
    )


def wb_alert_user_about_in_stock(product: Product) -> str:
    logger.info(
        f"Продукт появился в наличии: {product.article} в количестве {product.count} штуки")
    return (
        f"<b>Товар появился в наличии</b> "
        f"<b>{product.brand} {product.name} {product.colors} </b> "
        f"<b>Цена:</b> {product.price} руб. "
        f"<b>Количество:</b> {product.count} шт. "
        f"<b>Артикул:</b> <code>{product.article}</code> "
        f"<b>Продавец:</b> <a href='https://www.wildberries.ru/seller/{product.supplier_id}'>{product.supplier}</a>\n"
        f"<a href='https://www.wildberries.ru/catalog/{product.article}/detail.aspx'>СТРАНИЦА ТОВАРА</a>"
    )


def wb_alert_user_about_out_stock(product: Product) -> str:
    logger.info(
        f"Продукт закончился: {product.article}")
    return (
        f"<b>Товар закончился</b> "
        f"<b>{product.brand} {product.name} {product.colors}</b> "
        f"<b>Артикул:</b> <code>{product.article}</code> "
        f"<b>Продавец:</b> <a href='https://www.wildberries.ru/seller/{product.supplier_id}'>{product.supplier}</a>\n"
        f"<a href='https://www.wildberries.ru/catalog/{product.article}/detail.aspx'>СТРАНИЦА ТОВАРА</a>"
    )


def wb_alert_user_about_not_found(old_product: Product) -> str:
    return (
        f"<b>Артикул товара не действителен</b>\n"
        f"Артикул <code>{old_product.article}</code> товара:\n"
        f"<b>{old_product.brand} {old_product.name} {old_product.colors}</b>\n"
        f"Больше не действителен.\n\n"
        f"Проверьте наличие товара на сайте по этому артикулу и добавьте в бота снова.\n"
    )
