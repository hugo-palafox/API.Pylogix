class PyLogixTag:
    def __init__(self, Name, Type,TypeValue,Status, Value, TimeStamp):
        self.Name = Name
        self.Type = Type        
        self.TypeValue=TypeValue
        self.Status = Status
        self.Value = Value
        self.TimeStamp = TimeStamp
class ToolAndPyLogixTagDTO:
    def __init__(self, tool_data, pylogix_tags):
        self.ToolData = tool_data
        self.PyLogixTags = pylogix_tags

class Tool:
     def __init__(self, Id=None, ToolId=None, ToolName=None, Product=None, ProductRev=None, Descri=None, PlcType=None, RackSlot=None, IpAddress=None, Step=None, Status=None, UpdBy=None, TimeStamp=None):
        self.Id = Id
        self.ToolId = ToolId
        self.ToolName = ToolName
        self.Product = Product
        self.ProductRev = ProductRev
        self.Descri = Descri
        self.PlcType = PlcType
        self.RackSlot = RackSlot
        self.IpAddress = IpAddress
        self.Step = Step
        self.Status = Status
        self.UpdBy = UpdBy
        self.TimeStamp = TimeStamp      