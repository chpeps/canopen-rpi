#!/usr/bin/python3
import CAN
import CANopen

CAN_INTERFACE = "vcan0"

can_bus = CAN.Bus(CAN_INTERFACE)

node_id = 0x01

canopen_od = CANopen.ObjectDictionary({ # TODO: Include data types so there is a way to determine the length of values for SDO responses (currently always 4 bytes)
    CANopen.ODI_DEVICE_TYPE: 0x00000000,
    CANopen.ODI_ERROR: 0x00,
    CANopen.ODI_SYNC: 0x40000000 + (CANopen.FUNCTION_CODE_SYNC << CANopen.FUNCTION_CODE_BITNUM),
    CANopen.ODI_SYNC_TIME: 0, # 32-bit, in us
    CANopen.ODI_EMCY_ID: (CANopen.FUNCTION_CODE_EMCY << CANopen.FUNCTION_CODE_BITNUM) + node_id,
    CANopen.ODI_HEARTBEAT_CONSUMER_TIME: CANopen.Object({
        CANopen.ODSI_VALUE: 1,
        CANopen.ODSI_HEARTBEAT_CONSUMER_TIME: 2000, # all nodes, 16-bit, in ms
    }),
    CANopen.ODI_HEARTBEAT_PRODUCER_TIME: 1000, # 16-bit, in ms
    CANopen.ODI_IDENTITY: CANopen.Object({
        CANopen.ODSI_VALUE: 4,
        CANopen.ODSI_IDENTITY_VENDOR: 0x00000000,
        CANopen.ODSI_IDENTITY_PRODUCT: 0x00000001,
        CANopen.ODSI_IDENTITY_REVISION: 0x00000000,
        CANopen.ODSI_IDENTITY_SERIAL: 0x00000001,
    }),
    CANopen.ODI_SDO_SERVER: CANopen.Object({
        CANopen.ODSI_VALUE: 2,
        CANopen.ODSI_SDO_SERVER_DEFAULT_CSID: (CANopen.FUNCTION_CODE_SDO_RX << CANopen.FUNCTION_CODE_BITNUM) + node_id,
        CANopen.ODSI_SDO_SERVER_DEFAULT_SCID: (CANopen.FUNCTION_CODE_SDO_TX << CANopen.FUNCTION_CODE_BITNUM) + node_id,
    }),
    CANopen.ODI_SDO_CLIENT: CANopen.Object({
        CANopen.ODSI_VALUE: 0, # Update when heartbeats received
    }),
    CANopen.ODI_TPDO1_COMMUNICATION_PARAMETER: CANopen.Object({
        CANopen.ODSI_VALUE: 2,
        CANopen.ODSI_TPDO_COMM_PARAM_ID: (1 << CANopen.TPDO_COMM_PARAM_ID_RTR_BITNUM) + node_id,
        CANopen.ODSI_TPDO_COMM_PARAM_TYPE: 0xFD, # RTR-only, asynchronous
    }),
    CANopen.ODI_TPDO1_MAPPING_PARAMETER: CANopen.Object({
        CANopen.ODSI_VALUE: 2,
        0x01: (CANopen.ODI_SYNC << 16) + (CANopen.ODSI_VALUE << 8) + 32,
        0x02: (CANopen.ODI_SYNC_TIME << 16) + (CANopen.ODSI_VALUE << 8) + 32,
    }),
})

node = CANopen.Node(can_bus, node_id, canopen_od)
node.boot()
node.listen()
