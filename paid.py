import os

from yoomoney import Client, Authorize, Quickpay

token = os.getenv('YOOMONEY_TOKEN')
client = Client(token)
user = client.account_info()
print("Account number:", user.account)
print("Account balance:", user.balance)
print("Account currency code in ISO 4217 format:", user.currency)
print("Account status:", user.account_status)
print("Account type:", user.account_type)
print("Extended balance information:")
for pair in vars(user.balance_details):
    print("\t-->", pair, ":", vars(user.balance_details).get(pair))
print("Information about linked bank cards:")
cards = user.cards_linked
if len(cards) != 0:
    for card in cards:
        print(card.pan_fragment, " - ", card.type)
else:
    print("No card is linked to the account")

quickpay = Quickpay(
            receiver=os.getenv('WALLET'),
            quickpay_form="shop",
            targets="Sponsor this project",
            paymentType="SB",
            sum=100,
            label="user_test"
            )
print(quickpay.base_url)
print(quickpay.redirected_url)

print("List of operations:")
history = client.operation_history(label="user_test")
print("Next page starts with: ", history.next_record)
for operation in history.operations:
    print()
    print("Operation:",operation.operation_id)
    print("\tStatus     -->", operation.status)
    print("\tDatetime   -->", operation.datetime)
    print("\tTitle      -->", operation.title)
    print("\tPattern id -->", operation.pattern_id)
    print("\tDirection  -->", operation.direction)
    print("\tAmount     -->", operation.amount)
    print("\tLabel      -->", operation.label)
    print("\tType       -->", operation.type)