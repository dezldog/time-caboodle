from gpsdclient import GPSDClient

client = GPSDClient(host="127.0.0.1")

for result in client.dict_stream(convert_datetime=True):
    if result["class"] == "TPV":
        FIX=result.get("mode")
        print(FIX)
        break
