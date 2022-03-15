def getEvent(contract, event, start_block, **kwargs):
    print(kwargs)

getEvent(contract="", event="",start_block="123",end_block="123")

CONTRACT = {
    "getEvent": "getEvent"
}
print(CONTRACT["getEvent"](contract="", event="",start_block="123",end_block="123"))