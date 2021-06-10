import visa

# rm = visa.ResourceManager('@py')
rm = visa.ResourceManager()
print(list(rm.list_resources()))

