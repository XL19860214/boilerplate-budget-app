class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []
        self.cursor = -1
        self.balance = 0


    def deposit(self, amount, description = ''):
        self.ledger.append({'amount': amount, 'description': description})


    def withdraw(self, amount, description = ''):
        if self.check_funds(amount):
            self.ledger.append({'amount': -1 * amount, 'description': description})
            return True
        return False


    def get_balance(self):
        if self.cursor == len(self.ledger) - 1:
            return self.balance

        for i, item in enumerate(self.ledger):
            if i <= self.cursor:
                continue
            self.balance += item['amount']
        self.cursor = len(self.ledger) - 1

        return self.balance

    
    def transfer(self, amount, category):
        if self.check_funds(amount):
            if self.withdraw(amount, 'Transfer to ' + category.name):
                category.deposit(amount, 'Transfer from ' + self.name)
                return True
        return False

    
    def check_funds(self, amount):
        if amount <= self.get_balance():
            return True
        return False


    def __str__(self):
        titleWidth = 30
        nameLength = len(self.name)
        titlePrefixLength = (titleWidth - nameLength) // 2
        titlePrefix = '*' * titlePrefixLength
        title = titlePrefix + self.name + '*' * (titleWidth - titlePrefixLength - nameLength)
        
        output = title + '\n'

        for item in self.ledger:
            line = '{:s}{:>7.2f}'.format(item['description'].ljust(23)[:23], item['amount'])
            output += line + '\n'

        output += 'Total: {:.2f}'.format(self.get_balance())

        return output


def create_spend_chart(categories):
    spends = {}
    total = 0
    maxCategoryNameLength = 0
    for category in categories:
        spend = 0
        for item in category.ledger:
            if item['amount'] < 0:
                spend += item['amount']
        spend *= -1
        spends[category.name] = {'spend': spend}
        total += spend

        if len(category.name) > maxCategoryNameLength:
            maxCategoryNameLength = len(category.name)

    categoriesLength = len(categories)

    canvas = [[' '] * (5 + categoriesLength * 3) for i in range(12 + maxCategoryNameLength)]

    for i, percentage in enumerate(range(0, 101, 10)[::-1]):
        percentageStr = str(percentage)
        canvas[i][3 - len(percentageStr):3] = list(percentageStr)
        canvas[i][3] = '|'

    canvas[11][4:] = list('-' * (len(canvas[11]) - 4))

    x = 5
    y = 12
    for i, category in enumerate(categories):
        for j, char in enumerate(category.name):
            canvas[y + j][x + i * 3] = char
        r = int(spends[category.name]['spend'] / total * 100)
        if r % 10 == 0:
            r += 1
        for k, percentage in enumerate(range(0, r, 10)):
            canvas[y - 2 - k][x + i * 3] = 'o'

    output = 'Percentage spent by category' + '\n'

    for i, line in enumerate(canvas):
        output += ''.join(line)
        if i < len(canvas) - 1:
            output += '\n'
    
    return output
