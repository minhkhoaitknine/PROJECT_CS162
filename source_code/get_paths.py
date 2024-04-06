import csv
import json
from pyproj import Proj, transform

def Transformer(lng, lat): #x, y= Transformer(lng, lat)
    input_proj = Proj(init='epsg:4326')  # WGS 84 (hệ tọa độ toàn cầu)
    output_proj = Proj(init='epsg:3857')  # Web Mercator (hệ tọa độ sử dụng bởi hầu hết các bản đồ web)
    return transform(input_proj, output_proj, lng, lat)

class Path:
    def __init__(self, data):
        self.lat = data['lat']
        self.lng = data['lng']
        self.RouteId = int(data['RouteId'])
        self.RouteVarId = int(data['RouteVarId'])
        
    def SetAttribute(self,attribute, value):
        setattr(self, attribute, value)
        
    def GetAttribute(self,attribute):
        return getattr(self, attribute)
    
class PathQuery:
    def __init__(self, file_path):
        self.paths = []
        with open(file_path, 'r',encoding='utf-8') as file:
            for line in file:
                data = json.loads(line)
                Path(data)
                self.paths.append(Path(data))
                
                
    
    def searchByAttributes(self, **kwargs):
        results = []
        for pth in self.paths:
            match = True
            for attribute, value in kwargs.items():
                if pth.GetAttribute(attribute) != value:
                    match = False
                    break
            if match==True:
                results.append(pth)
        return results
    
    def outputAsCSV(self, paths, filename):  # Modify method signature
        fieldnames = ['lat', 'lng', 'RouteId', 'RouteVarId']

        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:  # Specify UTF-8 encoding
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for path in paths:
                writer.writerow(path.__dict__)
                
    def outputAsJSON(self, paths, filename):
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            for path in paths:
                json.dump(path.__dict__, jsonfile, ensure_ascii=False)
                jsonfile.write('\n')
    
def main():
    query=PathQuery('D:/study/term_2/CS162/Lab/repository/PROJECT_CS162/source_code/paths.json')
    query.outputAsCSV(query.searchByAttributes(RouteId=303),'paths_CSV_file')
    query.outputAsJSON(query.searchByAttributes(RouteId=23, RouteVarId=45),'paths_JSON_file')
if __name__=="__main__": 
    main() 