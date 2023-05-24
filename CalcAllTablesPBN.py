#! /usr/bin/python

import dds
import ctypes
import hands
import functions

DDdealsPBN = dds.ddTableDealsPBN()
tableRes = dds.ddTablesRes()
pres = dds.allParResults()

# mode = 0
# tFilter = ctypes.c_int * dds.DDS_STRAINS
# trumpFilter = tFilter(0, 0, 0, 0, 0)
# line = ctypes.create_string_buffer(80)

# dds.SetMaxThreads(0)

# DDdealsPBN.noOfTables = 1

# for handno in range(1):
#     DDdealsPBN.deals[handno].cards = b"N:QJ6.K652.J85.T98 873.J97.AT764.Q4 K5.T83.KQ9.A7652 AT942.AQ4.32.KJ3"

# res = dds.CalcAllTablesPBN(ctypes.pointer(DDdealsPBN), mode, trumpFilter, ctypes.pointer(tableRes), ctypes.pointer(pres))

# if res != dds.RETURN_NO_FAULT:
#     dds.ErrorMessage(res, line)
#     print("DDS error: {}".format(line.value.decode("utf-8")))

# for handno in range(1):
#     match = functions.CompareTable(ctypes.pointer(tableRes.results[handno]), handno)

#     line = "CalcDDtable, hand {}: {}".format(
#         handno + 1,
#         "OK" if match else "ERROR")

#     functions.PrintPBNHand(line, DDdealsPBN.deals[handno].cards)

#     functions.PrintTable(ctypes.pointer(tableRes.results[handno]))

def calcdds(pbn_str, printout = False):
    # DDdealsPBN = dds.ddTableDealsPBN()
    # tableRes = dds.ddTablesRes()
    # pres = dds.allParResults()

    mode = 0
    tFilter = ctypes.c_int * dds.DDS_STRAINS
    trumpFilter = tFilter(0, 0, 0, 0, 0)
    line = ctypes.create_string_buffer(80)

    dds.SetMaxThreads(0)

    DDdealsPBN.noOfTables = 1

    DDdealsPBN.deals[0].cards = pbn_str.encode('utf-8')

    res = dds.CalcAllTablesPBN(ctypes.pointer(DDdealsPBN), mode, trumpFilter, ctypes.pointer(tableRes), ctypes.pointer(pres))
    if res != dds.RETURN_NO_FAULT:
        dds.ErrorMessage(res, line)
        print("DDS error: {}".format(line.value.decode("utf-8")))

    # match = functions.CompareTable(ctypes.pointer(tableRes.results[0]), 0)

    line = "CalcDDtable, hand {}: {}".format(
        1,
        "OK" )
    if printout:
        functions.PrintPBNHand(line, DDdealsPBN.deals[0].cards)

        functions.PrintTable(ctypes.pointer(tableRes.results[0]))

    result = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    for suit in range(5):
        for i in range(4):
            # if suit == 4:
                result[suit][i] = ctypes.pointer(tableRes.results[0]).contents.resTable[suit][i]
            # else:
                # result[3 - suit][i] = ctypes.pointer(tableRes.results[0]).contents.resTable[suit][i]
    print(result)
    return result