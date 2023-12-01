from pylogix import PLC

with PLC() as comm:
            comm.ProcessorSlot = 1
            comm.IPAddress = '192.168.120.131'
            tags = comm.GetTagList()
            tag_read = comm.Read('IOT_Tags_1')#, datatype=tag.TypeValue
            print(tag_read.Value)
            #print(comm.CIPTypes)
            print(comm.UDT)