from yoomoney import Client, Authorize, Quickpay


# Authorize(
#       client_id="59F9E0ED2DC91621E977DACDA42319338C0C02B7269C8DA16EDAB1BC7737652B",
#       redirect_uri="https://happypython.ru",
#       scope=["account-info",
#              "operation-history",
#              "operation-details",
#              "incoming-transfers",
#              "payment-p2p",
#              "payment-shop",
#              ]
#       )
token = "410015944168016.2166343A6A774D27ACEEDA48ADC9D63DA3E5AA26B6960724E9ACC150336360D3B1980C224B5165AA2B632BD05167870483F4C8024B2508FD90AD0159D0EAF5EF5B8230F6ED69914F249BF87760114EAF364EC4301C7F5A85477FA851D912DB269495AFB9A9CFF84E49D860027A026CD1207D95689043FDB1F58A8EA0524E6590"
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
            receiver="410015944168016",
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