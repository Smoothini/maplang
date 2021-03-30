import sys

sys.path.insert(0, '../..')
from sly import Lexer, Parser


class MapLexer(Lexer):

    tokens = { FLOAT, ID, CREATE, CREATEMAP, CREATEPOINT, DIR, DIRHANDLE, ASSIGN, COMMA, AND, AT, COORDINATE, EOL, SHOW }
    ignore = ' \t'
    
    CREATE = r'create'
    CREATEMAP = r'map'
    CREATEPOINT = r'point'
    SHOW = r'show'
    DIR = r'(right|up|down|left)'
    DIRHANDLE = r'(from|in)'
    AND = r'and'
    AT = r'at'
    COORDINATE = r'[(][+-]?([0-9]*[.])?[0-9]+[,][+-]?([0-9]*[.])?[0-9]+[)]'
    
    ID = r'[a-zA-Z][a-zA-Z0-9]*'
    FLOAT = r'[+-]?([0-9]*[.])?[0-9]+'

    ASSIGN = r'='
    COMMA = r','
    EOL = r';'

    # Error handling rule
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)


class MapParser(Parser):
    tokens = MapLexer.tokens

    def __init__(self):
        #self.names = { }
        self.maps = {}
        self.points = {}
        self.coordinates = {}

    @_('CREATE create EOL statement')
    def statement(self, p):
        pass

    ##just for testing purposes
    @_('SHOW ID')
    def statement(self, p):
        print(self.points[p.ID])
        print(self.coordinates[p.ID])
    

    @_('')
    def statement(self, p):
        pass

    @_('CREATEMAP createmap')
    def create(self, p):
        pass
        
    @_('CREATEPOINT createpoint')
    def create(self, p):
        pass

    @_('ASSIGN ID')
    def createmap(self, p):
        self.maps[p.ID] = f"Map {p.ID}"

    @_('ASSIGN ID')
    def createpoint(self, p):
        self.points[p.ID] = p.ID
        self.coordinates[p.ID] = (0.0, 0.0)
    
    @_('COMMA relation ASSIGN ID')
    def createpoint(self, p):
        #print(p.relation)
        self.points[p.ID] = p.ID
        if len(p.relation) == 2:
            x = float(p.relation[0])
            y = float(p.relation[1])
            self.coordinates[p.ID] = (x, y)
        elif len(p.relation) == 3:
            x, y = self.coordinates[p.relation[2]]
            val = float(p.relation[0])
            dirr = p.relation[1]
            if dirr == "right":
                x += val
            elif dirr == "left":
                x -= val
            elif dirr == "up":
                y += val
            elif dirr == "down":
                y -= val
            self.coordinates[p.ID] = (x, y)
        elif len(p.relation) == 5:
            print(p.relation)
            x, y = self.coordinates[p.relation[4]]
            val = float(p.relation[0])
            dirr = p.relation[1]
            if dirr == "right":
                x += val
            elif dirr == "left":
                x -= val
            elif dirr == "up":
                y += val
            elif dirr == "down":
                y -= val
            
            val = float(p.relation[2])
            dirr = p.relation[3]
            if dirr == "right":
                x += val
            elif dirr == "left":
                x -= val
            elif dirr == "up":
                y += val
            elif dirr == "down":
                y -= val
            self.coordinates[p.ID] = (x, y)
        print(self.coordinates[p.ID])
        
    @_('AT COORDINATE')
    def relation(self, p):
        txt = str(p.COORDINATE[1:-1])
        x,y = txt.strip().split(',')
        return x, y

    @_('FLOAT DIR reltype')
    def relation(self, p):
        if len(p.reltype) == 3:
            float2, dir2, fromid = p.reltype
            return p.FLOAT, p.DIR, float2, dir2, fromid
        else:
            return p.FLOAT, p.DIR, p.reltype

    @_('relationexplicit')
    def reltype(self, p):
        return p.relationexplicit

    @_('twodrelation')
    def reltype(self, p):
        return p.twodrelation
    
    @_('')
    def reltype(self, p):
        pass

    @_('DIRHANDLE ID')
    def relationexplicit(self, p):
        if p.ID not in self.points:
            print(f"Error: {p.ID} does not exist!")
        else:
            return p.ID
    
    @_('AND FLOAT DIR twodreltype')
    def twodrelation(self, p):
        return p.FLOAT, p.DIR, p.twodreltype

    @_('twodrelexplicit')
    def twodreltype(self, p):
        return p.twodrelexplicit

    @_('')
    def twodreltype(self, p):
        pass
    
    @_('DIRHANDLE ID')
    def twodrelexplicit(self, p):
        return p.ID


if __name__ == '__main__':
    lexer = MapLexer()
    parser = MapParser()
    data = 'create map = cassiopeia; ' \
           'create point = p1;' \
           'create point, 5.2 right from p1 = p2;'

    #for tok in lexer.tokenize(data):
     #   print(tok)

    while True:
        try:
            text = input('mapl> ')
        except EOFError:
            break
        if text:
            parser.parse(lexer.tokenize(text))
            #for tok in lexer.tokenize(text):
             #   print(tok)