from transliterate import translit
lit='desff123'
print(translit(f"{lit}", "ru", reversed=True))
print(translit(u"defc132", "ru", reversed=True))