from datetime import date, datetime

today = date.today()

d1 = today.strftime("%d/%m/%Y")

print(d1)

# Test the conversion

today_v2 = datetime.strptime(d1, '%d/%m/%Y')
print(today_v2.strftime("%d/%m/%Y"))