# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: net.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\tnet.proto\x12\x03Net\"*\n\x06Header\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12\x0e\n\x06\x63\x61r_id\x18\x02 \x01(\x06\"\x1b\n\x07Message\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\"\x96\x01\n\x0fRegisterRequest\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12-\n\x07payload\x18\x02 \x01(\x0b\x32\x1c.Net.RegisterRequest.Payload\x12\x0e\n\x06\x63\x61r_id\x18\x03 \x01(\x0c\x1a\x32\n\x07Payload\x12\x10\n\x08\x63\x61r_type\x18\x01 \x01(\x0c\x12\x15\n\rregister_code\x18\x02 \x01(\x0c\"\xaf\x01\n\x0cLoginRequest\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12*\n\x07payload\x18\x02 \x01(\x0b\x32\x19.Net.LoginRequest.Payload\x12\x0e\n\x06\x63\x61r_id\x18\x03 \x01(\x0c\x1aQ\n\x07Payload\x12\x14\n\x0clogin_reason\x18\x01 \x01(\x0c\x12\x0f\n\x07task_id\x18\x02 \x01(\x0c\x12\x0c\n\x04sign\x18\x03 \x01(\x03\x12\x11\n\ttimestamp\x18\x04 \x01(\x03\"u\n\tHeartbeat\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12\'\n\x07payload\x18\x02 \x01(\x0b\x32\x16.Net.Heartbeat.Payload\x12\x0e\n\x06\x63\x61r_id\x18\x03 \x01(\x0c\x1a\x1d\n\x07Payload\x12\x12\n\nlive_state\x18\x01 \x01(\x0c\"\x81\x08\n\x0bStateReport\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12)\n\x07payload\x18\x02 \x01(\x0b\x32\x18.Net.StateReport.Payload\x12\x0e\n\x06\x63\x61r_id\x18\x03 \x01(\x0c\x12\x11\n\ttimestamp\x18\x04 \x01(\x03\x1a\x91\x07\n\x07Payload\x12\x13\n\x0b\x63heck_state\x18\x01 \x01(\r\x12\x16\n\x0ehardwire_state\x18\x02 \x01(\r\x12\x15\n\rdriving_state\x18\x03 \x01(\r\x12\x11\n\tlongitude\x18\x04 \x01(\x01\x12\x10\n\x08latitude\x18\x05 \x01(\x01\x12\r\n\x05speed\x18\x06 \x01(\x02\x12\x0f\n\x07mileage\x18\x07 \x01(\x02\x12\x0f\n\x07\x62\x61ttery\x18\x08 \x01(\r\x12\x0f\n\x07voltage\x18\t \x01(\x02\x12\x0f\n\x07\x63urrent\x18\n \x01(\x02\x12\x1b\n\x13\x61verage_temperature\x18\x0b \x01(\x02\x12\x1c\n\x14max_cell_temperature\x18\x0c \x01(\x02\x12\x1c\n\x14min_cell_temperature\x18\r \x01(\x02\x12\x18\n\x10max_cell_voltage\x18\x0e \x01(\x02\x12\x18\n\x10min_cell_voltage\x18\x0f \x01(\x02\x12\x15\n\rlocal_task_id\x18\x10 \x01(\x0c\x12\x18\n\x10platform_task_id\x18\x11 \x01(\x0c\x12\x16\n\x0e\x63\x61rlock_status\x18\x12 \x01(\x08\x12\x15\n\rrest_distance\x18\x13 \x01(\x02\x12\x17\n\x0f\x63harging_status\x18\x14 \x01(\x08\x12\x12\n\nturn_light\x18\x15 \x01(\r\x12\x16\n\x0e\x63urtained_door\x18\x16 \x01(\r\x12\x12\n\ncargo_rear\x18\x17 \x01(\r\x12\x13\n\x0b\x63\x61rgo_front\x18\x18 \x01(\r\x12\t\n\x01x\x18\x19 \x01(\x01\x12\t\n\x01y\x18\x1a \x01(\x01\x12\x11\n\tauto_scan\x18\x1b \x01(\x08\x12\x19\n\x11warn_light_status\x18\x1c \x01(\x08\x12\x1b\n\x13\x64isinfection_status\x18\x1d \x01(\x08\x12\x14\n\x0cliquid_level\x18\x1f \x01(\r\x12\x10\n\x08\x61udio_id\x18  \x01(\t\x12\x16\n\x0e\x61udio_progress\x18! \x01(\r\x12\x13\n\x0b\x63ruise_name\x18\" \x01(\r\x12\x17\n\x0f\x63\x61pture_pattern\x18# \x01(\r\x12\x14\n\x0cis_camera_on\x18$ \x01(\x08\x12\x16\n\x0eis_localrecord\x18% \x01(\x08\x12\x17\n\x0flow_beam_status\x18& \x01(\x08\x12\x0c\n\x04mode\x18\' \x01(\r\x12\x13\n\x0bpush_status\x18( \x01(\x08\x12(\n\rcabinet_state\x18) \x01(\x0b\x32\x11.Net.CabinetState\x12\x0c\n\x04sign\x18* \x01(\x04\"\x99\x01\n\tStartTask\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12\'\n\x07payload\x18\x02 \x01(\x0b\x32\x16.Net.StartTask.Payload\x12\x0e\n\x06\x63\x61r_id\x18\x03 \x01(\x0c\x1a\x41\n\x07Payload\x12\x0f\n\x07task_id\x18\x01 \x01(\x0c\x12\x12\n\nstart_time\x18\x02 \x01(\x06\x12\x11\n\ttask_type\x18\x03 \x01(\r\"\xb9\x01\n\x07\x45ndTask\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12%\n\x07payload\x18\x02 \x01(\x0b\x32\x14.Net.EndTask.Payload\x12\x0e\n\x06\x63\x61r_id\x18\x03 \x01(\x0c\x1a\x65\n\x07Payload\x12\x10\n\x08\x65nd_type\x18\x01 \x01(\r\x12\x12\n\nend_reason\x18\x02 \x01(\r\x12\x0f\n\x07task_id\x18\x03 \x01(\x0c\x12\x10\n\x08\x65nd_time\x18\x04 \x01(\x06\x12\x11\n\ttask_type\x18\x05 \x01(\r\"\xee\x01\n\x0eTakeOverReport\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12,\n\x07payload\x18\x02 \x01(\x0b\x32\x1b.Net.TakeOverReport.Payload\x12\x0e\n\x06\x63\x61r_id\x18\x03 \x01(\x0c\x1a\x8b\x01\n\x07Payload\x12\x15\n\rtakeover_type\x18\x01 \x01(\x0c\x12\x15\n\rlocal_task_id\x18\x02 \x01(\x0c\x12\x18\n\x10platform_task_id\x18\x03 \x01(\x0c\x12\x13\n\x0b\x63heck_state\x18\x04 \x01(\r\x12\x11\n\tlongitude\x18\x05 \x01(\x01\x12\x10\n\x08latitude\x18\x06 \x01(\x01\"\xc9\x01\n\x0b\x43heckReport\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12)\n\x07payload\x18\x02 \x01(\x0b\x32\x18.Net.CheckReport.Payload\x12\x0e\n\x06\x63\x61r_id\x18\x03 \x01(\x0c\x1am\n\x07Payload\x12\x14\n\x0c\x63heck_result\x18\x01 \x01(\x0c\x12\x16\n\x0ehardwire_state\x18\x02 \x01(\r\x12\x0f\n\x07\x62\x61ttery\x18\x03 \x01(\r\x12\x11\n\tlongitude\x18\x04 \x01(\x01\x12\x10\n\x08latitude\x18\x05 \x01(\x01\"\x80\x01\n\rLogoutRequest\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12+\n\x07payload\x18\x02 \x01(\x0b\x32\x1a.Net.LogoutRequest.Payload\x12\x0e\n\x06\x63\x61r_id\x18\x03 \x01(\x0c\x1a \n\x07Payload\x12\x15\n\rlogout_reason\x18\x01 \x01(\x0c\"\xa6\x01\n\x0b\x44rivingWarn\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12)\n\x07payload\x18\x02 \x01(\x0b\x32\x18.Net.DrivingWarn.Payload\x12\x0e\n\x06\x63\x61r_id\x18\x03 \x01(\x0c\x1aJ\n\x07Payload\x12\x13\n\x0b\x63heck_state\x18\x01 \x01(\r\x12\x15\n\rdriving_state\x18\x02 \x01(\r\x12\x13\n\x0b\x65rror_level\x18\x03 \x01(\r\"\xa9\x01\n\x0cHardwareWarn\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12*\n\x07payload\x18\x02 \x01(\x0b\x32\x19.Net.HardwareWarn.Payload\x12\x0e\n\x06\x63\x61r_id\x18\x03 \x01(\x0c\x1aK\n\x07Payload\x12\x13\n\x0b\x63heck_state\x18\x01 \x01(\r\x12\x16\n\x0ehardwire_state\x18\x02 \x01(\r\x12\x13\n\x0b\x65rror_level\x18\x03 \x01(\r\"\xc9\x02\n\x0cPlannedRoute\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12*\n\x07payload\x18\x02 \x01(\x0b\x32\x19.Net.PlannedRoute.Payload\x12\x0e\n\x06\x63\x61r_id\x18\x03 \x01(\x0c\x1a\xea\x01\n\x07Payload\x12\x15\n\rlocal_task_id\x18\x01 \x01(\x0c\x12\x18\n\x10platform_task_id\x18\x02 \x01(\x0c\x12\r\n\x05\x63ount\x18\x03 \x01(\r\x12\x32\n\x05nodes\x18\x04 \x03(\x0b\x32#.Net.PlannedRoute.Payload.RouteNode\x12\x11\n\ttask_type\x18\x05 \x01(\r\x12\x15\n\rrest_distance\x18\x06 \x01(\x02\x1a\x41\n\tRouteNode\x12\x11\n\tlongitude\x18\x01 \x01(\x01\x12\x10\n\x08latitude\x18\x02 \x01(\x01\x12\x0f\n\x07rank_no\x18\x03 \x01(\r\"\x91\x02\n\x07TaskCmd\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12%\n\x07payload\x18\x02 \x01(\x0b\x32\x14.Net.TaskCmd.Payload\x1a\xcc\x01\n\x07Payload\x12\x11\n\ttask_type\x18\x01 \x01(\r\x12\x0f\n\x07task_id\x18\x02 \x01(\x0c\x12\x13\n\x0bstart_point\x18\x03 \x01(\r\x12\x13\n\x0b\x64\x65stination\x18\x04 \x01(\r\x12\t\n\x01x\x18\x05 \x01(\x01\x12\t\n\x01y\x18\x06 \x01(\x01\x12\t\n\x01z\x18\t \x01(\x01\x12\x0b\n\x03yaw\x18\x07 \x01(\x01\x12\x18\n\x10\x64\x65stination_name\x18\x08 \x01(\t\x12\x14\n\x0cmain_task_id\x18\n \x01(\x0c\x12\x15\n\rstopping_time\x18\x0b \x01(\x03\"\xef\x01\n\x0fTaskCmdResponse\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12-\n\x07payload\x18\x02 \x01(\x0b\x32\x1c.Net.TaskCmdResponse.Payload\x12\x0e\n\x06\x63\x61r_id\x18\x03 \x01(\x0c\x1a\x8a\x01\n\x07Payload\x12\x0f\n\x07task_id\x18\x01 \x01(\x0c\x12\x0e\n\x06result\x18\x02 \x01(\x0c\x12\x15\n\rrefuse_reason\x18\x03 \x01(\x0c\x12\x11\n\ttask_type\x18\x04 \x01(\r\x12\x11\n\ttimestamp\x18\x05 \x01(\x03\x12!\n\x19global_plan_failed_reason\x18\x06 \x01(\r\"\xc5\x01\n\tCancelCmd\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12\'\n\x07payload\x18\x02 \x01(\x0b\x32\x16.Net.CancelCmd.Payload\x1a}\n\x07Payload\x12\x13\n\x0b\x63\x61ncel_type\x18\x01 \x01(\r\x12\x0f\n\x07task_id\x18\x02 \x01(\x0c\x12\x11\n\ttask_type\x18\x03 \x01(\r\x12\x0e\n\x06\x65xpire\x18\x04 \x01(\x03\x12\x11\n\ttimestamp\x18\x05 \x01(\x03\x12\x16\n\x0ereq_command_id\x18\x06 \x01(\x0c\"~\n\x03\x41\x43K\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12!\n\x07payload\x18\x02 \x01(\x0b\x32\x10.Net.ACK.Payload\x12\x0e\n\x06\x63\x61r_id\x18\x03 \x01(\x0c\x1a\x32\n\x07Payload\x12\x0e\n\x06result\x18\x01 \x01(\x0c\x12\x17\n\x0ftimestamp_delta\x18\x02 \x01(\x03\"\xc5\x01\n\x07LockCmd\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12%\n\x07payload\x18\x02 \x01(\x0b\x32\x14.Net.LockCmd.Payload\x1a\x80\x01\n\x07Payload\x12\x16\n\x0ereq_command_id\x18\x01 \x01(\x0c\x12\x14\n\x0coperation_id\x18\x02 \x01(\t\x12\x16\n\x0e\x61\x63\x63\x65ssory_type\x18\x03 \x01(\r\x12\x14\n\x0c\x61\x63\x63\x65ssory_id\x18\x04 \x01(\r\x12\x19\n\x11\x63ontrol_operation\x18\x05 \x01(\r\"\x94\x01\n\rRemoteControl\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12+\n\x07payload\x18\x02 \x01(\x0b\x32\x1a.Net.RemoteControl.Payload\x1a\x44\n\x07Payload\x12\x11\n\toperation\x18\x01 \x01(\x08\x12\x16\n\x0ereq_command_id\x18\x02 \x01(\x0c\x12\x0e\n\x06reason\x18\x03 \x01(\t\"\x83\x01\n\x07Msg_ACK\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12%\n\x07payload\x18\x02 \x01(\x0b\x32\x14.Net.Msg_ACK.Payload\x12\x0e\n\x06\x63\x61r_id\x18\x03 \x01(\x0c\x1a/\n\x07Payload\x12\x14\n\x0c\x61\x63k_class_id\x18\x01 \x01(\r\x12\x0e\n\x06result\x18\x02 \x01(\x0c\"\xe2\x01\n\x0cRoadBlockCmd\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12*\n\x07payload\x18\x02 \x01(\x0b\x32\x19.Net.RoadBlockCmd.Payload\x1a\x93\x01\n\x07Payload\x12\x11\n\toperation\x18\x01 \x01(\x08\x12\x37\n\nroadblocks\x18\x02 \x03(\x0b\x32#.Net.RoadBlockCmd.Payload.RoadBlock\x1a<\n\tRoadBlock\x12\n\n\x02id\x18\x01 \x01(\x03\x12\x11\n\tlongitude\x18\x02 \x01(\x01\x12\x10\n\x08latitude\x18\x03 \x01(\x01\"\xb3\x01\n\x07\x45rrWarn\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12%\n\x07payload\x18\x02 \x01(\x0b\x32\x14.Net.ErrWarn.Payload\x12\x0e\n\x06\x63\x61r_id\x18\x03 \x01(\x0c\x1a_\n\x07Payload\x12+\n\x05nodes\x18\x01 \x03(\x0b\x32\x1c.Net.ErrWarn.Payload.ErrCode\x1a\'\n\x07\x45rrCode\x12\x0c\n\x04\x63ode\x18\x01 \x01(\t\x12\x0e\n\x06\x64\x65tail\x18\x02 \x01(\t\"\xe3\x01\n\tOperation\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12\'\n\x07payload\x18\x02 \x01(\x0b\x32\x16.Net.Operation.Payload\x1a\x9a\x01\n\x07Payload\x12\x0c\n\x04type\x18\x01 \x01(\x05\x12\x0f\n\x07task_id\x18\x02 \x01(\x0c\x12\x16\n\x0ereq_command_id\x18\x03 \x01(\x0c\x12\x0e\n\x06\x65xpire\x18\x04 \x01(\x03\x12\x11\n\ttimestamp\x18\x05 \x01(\x03\x12\x1b\n\x13\x65nable_control_mode\x18\x06 \x03(\x05\x12\x18\n\x10operation_string\x18\x07 \x01(\t\"\x97\x01\n\rControlReport\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12+\n\x07payload\x18\x02 \x01(\x0b\x32\x1a.Net.ControlReport.Payload\x12\x0e\n\x06\x63\x61r_id\x18\x03 \x01(\x0c\x1a\x37\n\x07Payload\x12\x0f\n\x07task_id\x18\x01 \x01(\x0c\x12\r\n\x05\x65vent\x18\x02 \x01(\r\x12\x0c\n\x04type\x18\x03 \x01(\r\"f\n\nAppInfoCmd\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12(\n\x07payload\x18\x02 \x01(\x0b\x32\x17.Net.AppInfoCmd.Payload\x1a\x1c\n\x07Payload\x12\x11\n\toperation\x18\x01 \x01(\x08\"\xda\x01\n\rAppInfoReport\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12/\n\tsoftwares\x18\x02 \x01(\x0b\x32\x1c.Net.AppInfoReport.Softwares\x1a\x85\x01\n\tSoftwares\x12\r\n\x05\x63ount\x18\x01 \x01(\r\x12\x39\n\x05nodes\x18\x02 \x03(\x0b\x32*.Net.AppInfoReport.Softwares.SoftwaresNode\x1a.\n\rSoftwaresNode\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\t\"\x9a\x02\n\rAppInstallCmd\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12\'\n\x05items\x18\x02 \x01(\x0b\x32\x18.Net.AppInstallCmd.Items\x1a\xcd\x01\n\x05Items\x12\r\n\x05\x63ount\x18\x01 \x01(\r\x12\x31\n\x05nodes\x18\x02 \x03(\x0b\x32\".Net.AppInstallCmd.Items.ItemsNode\x1a\x81\x01\n\tItemsNode\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0f\n\x07is_soft\x18\x02 \x01(\x08\x12\x11\n\toperation\x18\x03 \x01(\r\x12\x11\n\tconf_name\x18\x04 \x01(\t\x12\x0c\n\x04text\x18\x05 \x01(\t\x12\x11\n\tsoft_name\x18\x06 \x01(\t\x12\x10\n\x08identity\x18\x07 \x01(\t\"\x8a\x02\n\x10\x41ppInstallReport\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12*\n\x05items\x18\x02 \x01(\x0b\x32\x1b.Net.AppInstallReport.Items\x1a\xb7\x01\n\x05Items\x12\r\n\x05\x63ount\x18\x01 \x01(\r\x12\x34\n\x05nodes\x18\x02 \x03(\x0b\x32%.Net.AppInstallReport.Items.ItemsNode\x1ai\n\tItemsNode\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0f\n\x07is_soft\x18\x02 \x01(\x08\x12\x11\n\toperation\x18\x03 \x01(\r\x12\n\n\x02ok\x18\x04 \x01(\x08\x12\x0e\n\x06reason\x18\x05 \x01(\t\x12\x10\n\x08identity\x18\x06 \x01(\t\"\xaf\x01\n\rManualControl\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12+\n\x07payload\x18\x02 \x01(\x0b\x32\x1a.Net.ManualControl.Payload\x1a_\n\x07Payload\x12\r\n\x05value\x18\x01 \x01(\r\x12\r\n\x05speed\x18\x02 \x01(\r\x12\x0e\n\x06status\x18\x03 \x01(\r\x12\x0e\n\x06result\x18\x04 \x01(\x08\x12\x16\n\x0ereq_command_id\x18\x05 \x01(\x0c\"\xa4\x01\n\x0ePresetPosition\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12,\n\x07payload\x18\x02 \x01(\x0b\x32\x1b.Net.PresetPosition.Payload\x1aR\n\x07Payload\x12\x0c\n\x04name\x18\x01 \x01(\r\x12\x11\n\toperation\x18\x02 \x01(\r\x12\x0e\n\x06result\x18\x03 \x01(\x08\x12\x16\n\x0ereq_command_id\x18\x04 \x01(\x0c\"\xad\x01\n\x06\x43ruise\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12$\n\x07payload\x18\x02 \x01(\x0b\x32\x13.Net.Cruise.Payload\x1ak\n\x07Payload\x12\x0b\n\x03\x63md\x18\x01 \x01(\r\x12\r\n\x05route\x18\x02 \x01(\r\x12\r\n\x05point\x18\x03 \x01(\r\x12\r\n\x05speed\x18\x04 \x01(\r\x12\x0e\n\x06result\x18\x05 \x01(\x08\x12\x16\n\x0ereq_command_id\x18\x06 \x01(\x0c\"\x8c\x01\n\nCarControl\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12(\n\x07payload\x18\x02 \x01(\x0b\x32\x17.Net.CarControl.Payload\x1a\x42\n\x07Payload\x12\x0f\n\x07operate\x18\x01 \x01(\x08\x12\x0e\n\x06result\x18\x02 \x01(\x08\x12\x16\n\x0ereq_command_id\x18\x03 \x01(\x0c\"\xba\x01\n\x05\x41udio\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12#\n\x07payload\x18\x02 \x01(\x0b\x32\x12.Net.Audio.Payload\x1az\n\x07Payload\x12\x0f\n\x07\x61udioID\x18\x01 \x01(\t\x12\x0b\n\x03md5\x18\x02 \x01(\t\x12\r\n\x05times\x18\x03 \x01(\r\x12\x10\n\x08interval\x18\x04 \x01(\r\x12\x0f\n\x07operate\x18\x05 \x01(\x08\x12\x0e\n\x06result\x18\x06 \x01(\x08\x12\x0f\n\x07seconds\x18\x07 \x01(\x01\"\x8a\x01\n\x0b\x42lackLpnCmd\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12\r\n\x05\x63ount\x18\x02 \x01(\r\x12%\n\x05items\x18\x03 \x03(\x0b\x32\x16.Net.BlackLpnCmd.Items\x1a\x33\n\x05Items\x12\n\n\x02id\x18\x01 \x01(\x0c\x12\x11\n\toperation\x18\x02 \x01(\r\x12\x0b\n\x03lpn\x18\x03 \x01(\x0c\"\x99\x01\n\x13\x42lackLpnCmdResponse\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12\r\n\x05\x63ount\x18\x02 \x01(\r\x12-\n\x05items\x18\x03 \x03(\x0b\x32\x1e.Net.BlackLpnCmdResponse.Items\x1a\x32\n\x05Items\x12\n\n\x02id\x18\x01 \x01(\x0c\x12\x11\n\toperation\x18\x02 \x01(\r\x12\n\n\x02ok\x18\x03 \x01(\x08\"\xcc\x01\n\x0f\x41larmMenuReport\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12-\n\x07payload\x18\x02 \x01(\x0b\x32\x1c.Net.AlarmMenuReport.Payload\x1ax\n\x07Payload\x12\x12\n\nalarm_time\x18\x01 \x01(\x06\x12-\n\x03gps\x18\x02 \x01(\x0b\x32 .Net.AlarmMenuReport.Payload.GPS\x1a*\n\x03GPS\x12\x11\n\tlongitude\x18\x01 \x01(\x01\x12\x10\n\x08latitude\x18\x02 \x01(\x01\"\x87\x01\n\x17SwitchCapturePatternCmd\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12\x35\n\x07payload\x18\x02 \x01(\x0b\x32$.Net.SwitchCapturePatternCmd.Payload\x1a#\n\x07Payload\x12\n\n\x02id\x18\x01 \x01(\x0c\x12\x0c\n\x04type\x18\x02 \x01(\r\"\xa3\x01\n\x1fSwitchCapturePatternCmdResponse\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12=\n\x07payload\x18\x02 \x01(\x0b\x32,.Net.SwitchCapturePatternCmdResponse.Payload\x1a/\n\x07Payload\x12\n\n\x02id\x18\x01 \x01(\x0c\x12\x0c\n\x04type\x18\x02 \x01(\r\x12\n\n\x02ok\x18\x03 \x01(\x08\"\x1e\n\nCaptureCmd\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\"\x99\x01\n\rCaptureNotify\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12+\n\x07payload\x18\x02 \x01(\x0b\x32\x1a.Net.CaptureNotify.Payload\x1aI\n\x07Payload\x12\x0c\n\x04type\x18\x01 \x01(\r\x12\x0c\n\x04name\x18\x02 \x01(\x0c\x12\x0e\n\x06object\x18\x03 \x01(\x0c\x12\x12\n\nisblacklpn\x18\x04 \x01(\x08\"\x9c\x01\n\x0e\x41liyunAuthInfo\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12,\n\x07payload\x18\x02 \x01(\x0b\x32\x1b.Net.AliyunAuthInfo.Payload\x1aJ\n\x07Payload\x12\x11\n\toperation\x18\x01 \x01(\r\x12\x0c\n\x04rtmp\x18\x02 \x01(\x0c\x12\x0f\n\x07ossinfo\x18\x03 \x01(\x0c\x12\r\n\x05nonce\x18\x04 \x01(\x0c\"\x89\x01\n\x0cStationRoute\x12\n\n\x02id\x18\x01 \x01(\x03\x12\x0c\n\x04name\x18\x02 \x01(\x0c\x12\x0c\n\x04\x61rea\x18\x03 \x01(\x0c\x12\x11\n\tlongitude\x18\x04 \x01(\x01\x12\x10\n\x08latitude\x18\x05 \x01(\x01\x12\t\n\x01x\x18\x06 \x01(\x01\x12\t\n\x01y\x18\x07 \x01(\x01\x12\t\n\x01z\x18\x08 \x01(\x01\x12\x0b\n\x03yaw\x18\t \x01(\x01\"z\n\x0cRouteWayInfo\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12*\n\x07payload\x18\x02 \x01(\x0b\x32\x19.Net.RouteWayInfo.Payload\x1a,\n\x07Payload\x12!\n\x06routes\x18\x01 \x03(\x0b\x32\x11.Net.StationRoute\"l\n\x0eRouteWayReport\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12,\n\x07payload\x18\x02 \x01(\x0b\x32\x1b.Net.RouteWayReport.Payload\x1a\x1a\n\x07Payload\x12\x0f\n\x07task_id\x18\x01 \x01(\x0c\"t\n\tCarConfig\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12\'\n\x07payload\x18\x02 \x01(\x0b\x32\x16.Net.CarConfig.Payload\x1a,\n\x07Payload\x12\x0c\n\x04\x61rea\x18\x01 \x01(\x0c\x12\x13\n\x0busage_state\x18\x02 \x01(\x0c\"\x82\x01\n\x0bStateChange\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12)\n\x07payload\x18\x02 \x01(\x0b\x32\x18.Net.StateChange.Payload\x1a\x36\n\x07Payload\x12\x0c\n\x04\x61rea\x18\x01 \x01(\t\x12\x0e\n\x06\x63\x61r_id\x18\x02 \x01(\t\x12\r\n\x05state\x18\x03 \x01(\r\"\xce\x01\n\x08\x45\x43\x44State\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12&\n\x07payload\x18\x02 \x01(\x0b\x32\x15.Net.ECDState.Payload\x1a\x87\x01\n\x07Payload\x12\x35\n\x08\x63\x61\x62inets\x18\x01 \x03(\x0b\x32#.Net.ECDState.Payload.SingleCabinet\x1a\x45\n\rSingleCabinet\x12\n\n\x02id\x18\x01 \x01(\r\x12\x13\n\x0block_status\x18\x02 \x01(\r\x12\x13\n\x0b\x64oor_status\x18\x03 \x01(\r\"\x93\x02\n\x0e\x43\x61\x62inetControl\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12,\n\x07payload\x18\x02 \x01(\x0b\x32\x1b.Net.CabinetControl.Payload\x1a\xc0\x01\n\x07Payload\x12\x16\n\x0ereq_command_id\x18\x01 \x01(\x0c\x12\x14\n\x0coperation_id\x18\x02 \x01(\t\x12\x16\n\x0e\x61\x63\x63\x65ssory_type\x18\x03 \x01(\r\x12\x14\n\x0c\x61\x63\x63\x65ssory_id\x18\x04 \x01(\r\x12\x19\n\x11\x63ontrol_operation\x18\x05 \x01(\r\x12\x0e\n\x06\x65xpire\x18\x06 \x01(\x03\x12\x11\n\ttimestamp\x18\x07 \x01(\x03\x12\x1b\n\x13\x65nable_control_mode\x18\x08 \x03(\x05\"\x9d\x03\n\x0c\x43\x61\x62inetState\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12*\n\x07payload\x18\x02 \x01(\x0b\x32\x19.Net.CabinetState.Payload\x1aO\n\x12\x45lectricDoorObject\x12\x0f\n\x07\x64oor_id\x18\x01 \x01(\r\x12\x13\n\x0block_status\x18\x02 \x01(\r\x12\x13\n\x0b\x64oor_status\x18\x03 \x01(\r\x1a\x38\n\x10RollerDoorObject\x12\x0f\n\x07\x64oor_id\x18\x01 \x01(\r\x12\x13\n\x0b\x64oor_status\x18\x02 \x01(\r\x1a\xc3\x01\n\x07Payload\x12\x19\n\x11\x65lectric_door_num\x18\x01 \x01(\r\x12\x43\n\x15\x65\x63lectic_doors_status\x18\x02 \x03(\x0b\x32$.Net.CabinetState.ElectricDoorObject\x12\x17\n\x0froller_door_num\x18\x03 \x01(\r\x12?\n\x13roller_doors_status\x18\x04 \x03(\x0b\x32\".Net.CabinetState.RollerDoorObject\"\xb6\x01\n\x10TransportControl\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12.\n\x07payload\x18\x02 \x01(\x0b\x32\x1d.Net.TransportControl.Payload\x1a`\n\x07Payload\x12\x16\n\x0ereq_command_id\x18\x01 \x01(\x0c\x12\x16\n\x0eoperation_type\x18\x02 \x01(\r\x12\x14\n\x0c\x63\x61rgo_number\x18\x03 \x01(\r\x12\x0f\n\x07task_id\x18\x04 \x01(\t\"\xd2\x01\n\x14TransportControlResp\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12\x32\n\x07payload\x18\x02 \x01(\x0b\x32!.Net.TransportControlResp.Payload\x1at\n\x07Payload\x12\x18\n\x10operation_result\x18\x01 \x01(\x08\x12\x16\n\x0eoperation_type\x18\x02 \x01(\r\x12\x16\n\x0ereq_command_id\x18\x03 \x01(\x0c\x12\x0e\n\x06reason\x18\x04 \x01(\t\x12\x0f\n\x07task_id\x18\x05 \x01(\t\"\xf3\x03\n\x0fSelfCheckReport\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12-\n\x07payload\x18\x02 \x01(\x0b\x32\x1c.Net.SelfCheckReport.Payload\x1a\x9e\x03\n\x07Payload\x12!\n\x19\x63hassis_control_mode_code\x18\x01 \x01(\r\x12\x18\n\x10\x63heck_start_time\x18\x02 \x01(\x03\x12\x16\n\x0e\x63heck_end_time\x18\x03 \x01(\x03\x12\x12\n\ncheck_type\x18\x04 \x01(\r\x12\x16\n\x0ereq_command_id\x18\x05 \x01(\t\x12\x13\n\x0b\x63ommand_sta\x18\x06 \x01(\x08\x12\x11\n\tcheck_sta\x18\x07 \x01(\x08\x12\x1c\n\x14software_startup_sta\x18\x08 \x01(\x08\x12\x14\n\x0chardware_sta\x18\t \x01(\x08\x12\x12\n\nsystem_sta\x18\n \x01(\x08\x12\x10\n\x08\x61lgo_sta\x18\x0b \x01(\x08\x12\x10\n\x08mode_sta\x18\x0c \x01(\x08\x12\x42\n\x0b\x65rror_codes\x18\r \x03(\x0b\x32-.Net.SelfCheckReport.Payload.UnifiedErrorCode\x1a:\n\x10UnifiedErrorCode\x12\x12\n\nerror_code\x18\x01 \x01(\x0c\x12\x12\n\nerror_rank\x18\x02 \x01(\r\"\xe4\x01\n\rOperationResp\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12+\n\x07payload\x18\x02 \x01(\x0b\x32\x1a.Net.OperationResp.Payload\x1a\x93\x01\n\x07Payload\x12\x0c\n\x04type\x18\x01 \x01(\x05\x12\x0f\n\x07task_id\x18\x02 \x01(\x0c\x12\x16\n\x0ereq_command_id\x18\x03 \x01(\x0c\x12\x18\n\x10operation_result\x18\x04 \x01(\x08\x12\x0e\n\x06reason\x18\x05 \x01(\t\x12\x11\n\ttimestamp\x18\x06 \x01(\x03\x12\x14\n\x0c\x66\x61ilure_code\x18\x07 \x01(\x03\"\x92\x01\n\tTaskEvent\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12\'\n\x07payload\x18\x02 \x01(\x0b\x32\x16.Net.TaskEvent.Payload\x1aJ\n\x07Payload\x12\x0c\n\x04type\x18\x01 \x01(\x05\x12\r\n\x05state\x18\x02 \x01(\x05\x12\x11\n\ttimestamp\x18\x03 \x01(\x03\x12\x0f\n\x07task_id\x18\x04 \x01(\x0c\"\xc6\x02\n\x08SyncTask\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\r\x12&\n\x07payload\x18\x02 \x01(\x0b\x32\x15.Net.SyncTask.Payload\x1a^\n\x07SubTask\x12\x13\n\x0bsub_task_id\x18\x01 \x01(\x0c\x12\x17\n\x0fsub_task_status\x18\x02 \x01(\r\x12\x11\n\ttimestamp\x18\x03 \x01(\x03\x12\x12\n\ntask_event\x18\x04 \x01(\x03\x1a\x9f\x01\n\x07Payload\x12\x14\n\x0cmain_task_id\x18\x01 \x01(\x0c\x12\x18\n\x10main_task_status\x18\x02 \x01(\r\x12\x11\n\ttimestamp\x18\x03 \x01(\x03\x12\'\n\x08sub_task\x18\x04 \x03(\x0b\x32\x15.Net.SyncTask.SubTask\x12\x13\n\x0bsync_status\x18\x05 \x01(\x04\x12\x13\n\x0bsync_result\x18\x06 \x01(\x08\x42\x04Z\x02./b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'net_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z\002./'
  _globals['_HEADER']._serialized_start=18
  _globals['_HEADER']._serialized_end=60
  _globals['_MESSAGE']._serialized_start=62
  _globals['_MESSAGE']._serialized_end=89
  _globals['_REGISTERREQUEST']._serialized_start=92
  _globals['_REGISTERREQUEST']._serialized_end=242
  _globals['_REGISTERREQUEST_PAYLOAD']._serialized_start=192
  _globals['_REGISTERREQUEST_PAYLOAD']._serialized_end=242
  _globals['_LOGINREQUEST']._serialized_start=245
  _globals['_LOGINREQUEST']._serialized_end=420
  _globals['_LOGINREQUEST_PAYLOAD']._serialized_start=339
  _globals['_LOGINREQUEST_PAYLOAD']._serialized_end=420
  _globals['_HEARTBEAT']._serialized_start=422
  _globals['_HEARTBEAT']._serialized_end=539
  _globals['_HEARTBEAT_PAYLOAD']._serialized_start=510
  _globals['_HEARTBEAT_PAYLOAD']._serialized_end=539
  _globals['_STATEREPORT']._serialized_start=542
  _globals['_STATEREPORT']._serialized_end=1567
  _globals['_STATEREPORT_PAYLOAD']._serialized_start=654
  _globals['_STATEREPORT_PAYLOAD']._serialized_end=1567
  _globals['_STARTTASK']._serialized_start=1570
  _globals['_STARTTASK']._serialized_end=1723
  _globals['_STARTTASK_PAYLOAD']._serialized_start=1658
  _globals['_STARTTASK_PAYLOAD']._serialized_end=1723
  _globals['_ENDTASK']._serialized_start=1726
  _globals['_ENDTASK']._serialized_end=1911
  _globals['_ENDTASK_PAYLOAD']._serialized_start=1810
  _globals['_ENDTASK_PAYLOAD']._serialized_end=1911
  _globals['_TAKEOVERREPORT']._serialized_start=1914
  _globals['_TAKEOVERREPORT']._serialized_end=2152
  _globals['_TAKEOVERREPORT_PAYLOAD']._serialized_start=2013
  _globals['_TAKEOVERREPORT_PAYLOAD']._serialized_end=2152
  _globals['_CHECKREPORT']._serialized_start=2155
  _globals['_CHECKREPORT']._serialized_end=2356
  _globals['_CHECKREPORT_PAYLOAD']._serialized_start=2247
  _globals['_CHECKREPORT_PAYLOAD']._serialized_end=2356
  _globals['_LOGOUTREQUEST']._serialized_start=2359
  _globals['_LOGOUTREQUEST']._serialized_end=2487
  _globals['_LOGOUTREQUEST_PAYLOAD']._serialized_start=2455
  _globals['_LOGOUTREQUEST_PAYLOAD']._serialized_end=2487
  _globals['_DRIVINGWARN']._serialized_start=2490
  _globals['_DRIVINGWARN']._serialized_end=2656
  _globals['_DRIVINGWARN_PAYLOAD']._serialized_start=2582
  _globals['_DRIVINGWARN_PAYLOAD']._serialized_end=2656
  _globals['_HARDWAREWARN']._serialized_start=2659
  _globals['_HARDWAREWARN']._serialized_end=2828
  _globals['_HARDWAREWARN_PAYLOAD']._serialized_start=2753
  _globals['_HARDWAREWARN_PAYLOAD']._serialized_end=2828
  _globals['_PLANNEDROUTE']._serialized_start=2831
  _globals['_PLANNEDROUTE']._serialized_end=3160
  _globals['_PLANNEDROUTE_PAYLOAD']._serialized_start=2926
  _globals['_PLANNEDROUTE_PAYLOAD']._serialized_end=3160
  _globals['_PLANNEDROUTE_PAYLOAD_ROUTENODE']._serialized_start=3095
  _globals['_PLANNEDROUTE_PAYLOAD_ROUTENODE']._serialized_end=3160
  _globals['_TASKCMD']._serialized_start=3163
  _globals['_TASKCMD']._serialized_end=3436
  _globals['_TASKCMD_PAYLOAD']._serialized_start=3232
  _globals['_TASKCMD_PAYLOAD']._serialized_end=3436
  _globals['_TASKCMDRESPONSE']._serialized_start=3439
  _globals['_TASKCMDRESPONSE']._serialized_end=3678
  _globals['_TASKCMDRESPONSE_PAYLOAD']._serialized_start=3540
  _globals['_TASKCMDRESPONSE_PAYLOAD']._serialized_end=3678
  _globals['_CANCELCMD']._serialized_start=3681
  _globals['_CANCELCMD']._serialized_end=3878
  _globals['_CANCELCMD_PAYLOAD']._serialized_start=3753
  _globals['_CANCELCMD_PAYLOAD']._serialized_end=3878
  _globals['_ACK']._serialized_start=3880
  _globals['_ACK']._serialized_end=4006
  _globals['_ACK_PAYLOAD']._serialized_start=3956
  _globals['_ACK_PAYLOAD']._serialized_end=4006
  _globals['_LOCKCMD']._serialized_start=4009
  _globals['_LOCKCMD']._serialized_end=4206
  _globals['_LOCKCMD_PAYLOAD']._serialized_start=4078
  _globals['_LOCKCMD_PAYLOAD']._serialized_end=4206
  _globals['_REMOTECONTROL']._serialized_start=4209
  _globals['_REMOTECONTROL']._serialized_end=4357
  _globals['_REMOTECONTROL_PAYLOAD']._serialized_start=4289
  _globals['_REMOTECONTROL_PAYLOAD']._serialized_end=4357
  _globals['_MSG_ACK']._serialized_start=4360
  _globals['_MSG_ACK']._serialized_end=4491
  _globals['_MSG_ACK_PAYLOAD']._serialized_start=4444
  _globals['_MSG_ACK_PAYLOAD']._serialized_end=4491
  _globals['_ROADBLOCKCMD']._serialized_start=4494
  _globals['_ROADBLOCKCMD']._serialized_end=4720
  _globals['_ROADBLOCKCMD_PAYLOAD']._serialized_start=4573
  _globals['_ROADBLOCKCMD_PAYLOAD']._serialized_end=4720
  _globals['_ROADBLOCKCMD_PAYLOAD_ROADBLOCK']._serialized_start=4660
  _globals['_ROADBLOCKCMD_PAYLOAD_ROADBLOCK']._serialized_end=4720
  _globals['_ERRWARN']._serialized_start=4723
  _globals['_ERRWARN']._serialized_end=4902
  _globals['_ERRWARN_PAYLOAD']._serialized_start=4807
  _globals['_ERRWARN_PAYLOAD']._serialized_end=4902
  _globals['_ERRWARN_PAYLOAD_ERRCODE']._serialized_start=4863
  _globals['_ERRWARN_PAYLOAD_ERRCODE']._serialized_end=4902
  _globals['_OPERATION']._serialized_start=4905
  _globals['_OPERATION']._serialized_end=5132
  _globals['_OPERATION_PAYLOAD']._serialized_start=4978
  _globals['_OPERATION_PAYLOAD']._serialized_end=5132
  _globals['_CONTROLREPORT']._serialized_start=5135
  _globals['_CONTROLREPORT']._serialized_end=5286
  _globals['_CONTROLREPORT_PAYLOAD']._serialized_start=5231
  _globals['_CONTROLREPORT_PAYLOAD']._serialized_end=5286
  _globals['_APPINFOCMD']._serialized_start=5288
  _globals['_APPINFOCMD']._serialized_end=5390
  _globals['_APPINFOCMD_PAYLOAD']._serialized_start=4289
  _globals['_APPINFOCMD_PAYLOAD']._serialized_end=4317
  _globals['_APPINFOREPORT']._serialized_start=5393
  _globals['_APPINFOREPORT']._serialized_end=5611
  _globals['_APPINFOREPORT_SOFTWARES']._serialized_start=5478
  _globals['_APPINFOREPORT_SOFTWARES']._serialized_end=5611
  _globals['_APPINFOREPORT_SOFTWARES_SOFTWARESNODE']._serialized_start=5565
  _globals['_APPINFOREPORT_SOFTWARES_SOFTWARESNODE']._serialized_end=5611
  _globals['_APPINSTALLCMD']._serialized_start=5614
  _globals['_APPINSTALLCMD']._serialized_end=5896
  _globals['_APPINSTALLCMD_ITEMS']._serialized_start=5691
  _globals['_APPINSTALLCMD_ITEMS']._serialized_end=5896
  _globals['_APPINSTALLCMD_ITEMS_ITEMSNODE']._serialized_start=5767
  _globals['_APPINSTALLCMD_ITEMS_ITEMSNODE']._serialized_end=5896
  _globals['_APPINSTALLREPORT']._serialized_start=5899
  _globals['_APPINSTALLREPORT']._serialized_end=6165
  _globals['_APPINSTALLREPORT_ITEMS']._serialized_start=5982
  _globals['_APPINSTALLREPORT_ITEMS']._serialized_end=6165
  _globals['_APPINSTALLREPORT_ITEMS_ITEMSNODE']._serialized_start=6060
  _globals['_APPINSTALLREPORT_ITEMS_ITEMSNODE']._serialized_end=6165
  _globals['_MANUALCONTROL']._serialized_start=6168
  _globals['_MANUALCONTROL']._serialized_end=6343
  _globals['_MANUALCONTROL_PAYLOAD']._serialized_start=6248
  _globals['_MANUALCONTROL_PAYLOAD']._serialized_end=6343
  _globals['_PRESETPOSITION']._serialized_start=6346
  _globals['_PRESETPOSITION']._serialized_end=6510
  _globals['_PRESETPOSITION_PAYLOAD']._serialized_start=6428
  _globals['_PRESETPOSITION_PAYLOAD']._serialized_end=6510
  _globals['_CRUISE']._serialized_start=6513
  _globals['_CRUISE']._serialized_end=6686
  _globals['_CRUISE_PAYLOAD']._serialized_start=6579
  _globals['_CRUISE_PAYLOAD']._serialized_end=6686
  _globals['_CARCONTROL']._serialized_start=6689
  _globals['_CARCONTROL']._serialized_end=6829
  _globals['_CARCONTROL_PAYLOAD']._serialized_start=6763
  _globals['_CARCONTROL_PAYLOAD']._serialized_end=6829
  _globals['_AUDIO']._serialized_start=6832
  _globals['_AUDIO']._serialized_end=7018
  _globals['_AUDIO_PAYLOAD']._serialized_start=6896
  _globals['_AUDIO_PAYLOAD']._serialized_end=7018
  _globals['_BLACKLPNCMD']._serialized_start=7021
  _globals['_BLACKLPNCMD']._serialized_end=7159
  _globals['_BLACKLPNCMD_ITEMS']._serialized_start=7108
  _globals['_BLACKLPNCMD_ITEMS']._serialized_end=7159
  _globals['_BLACKLPNCMDRESPONSE']._serialized_start=7162
  _globals['_BLACKLPNCMDRESPONSE']._serialized_end=7315
  _globals['_BLACKLPNCMDRESPONSE_ITEMS']._serialized_start=7265
  _globals['_BLACKLPNCMDRESPONSE_ITEMS']._serialized_end=7315
  _globals['_ALARMMENUREPORT']._serialized_start=7318
  _globals['_ALARMMENUREPORT']._serialized_end=7522
  _globals['_ALARMMENUREPORT_PAYLOAD']._serialized_start=7402
  _globals['_ALARMMENUREPORT_PAYLOAD']._serialized_end=7522
  _globals['_ALARMMENUREPORT_PAYLOAD_GPS']._serialized_start=7480
  _globals['_ALARMMENUREPORT_PAYLOAD_GPS']._serialized_end=7522
  _globals['_SWITCHCAPTUREPATTERNCMD']._serialized_start=7525
  _globals['_SWITCHCAPTUREPATTERNCMD']._serialized_end=7660
  _globals['_SWITCHCAPTUREPATTERNCMD_PAYLOAD']._serialized_start=7625
  _globals['_SWITCHCAPTUREPATTERNCMD_PAYLOAD']._serialized_end=7660
  _globals['_SWITCHCAPTUREPATTERNCMDRESPONSE']._serialized_start=7663
  _globals['_SWITCHCAPTUREPATTERNCMDRESPONSE']._serialized_end=7826
  _globals['_SWITCHCAPTUREPATTERNCMDRESPONSE_PAYLOAD']._serialized_start=7779
  _globals['_SWITCHCAPTUREPATTERNCMDRESPONSE_PAYLOAD']._serialized_end=7826
  _globals['_CAPTURECMD']._serialized_start=7828
  _globals['_CAPTURECMD']._serialized_end=7858
  _globals['_CAPTURENOTIFY']._serialized_start=7861
  _globals['_CAPTURENOTIFY']._serialized_end=8014
  _globals['_CAPTURENOTIFY_PAYLOAD']._serialized_start=7941
  _globals['_CAPTURENOTIFY_PAYLOAD']._serialized_end=8014
  _globals['_ALIYUNAUTHINFO']._serialized_start=8017
  _globals['_ALIYUNAUTHINFO']._serialized_end=8173
  _globals['_ALIYUNAUTHINFO_PAYLOAD']._serialized_start=8099
  _globals['_ALIYUNAUTHINFO_PAYLOAD']._serialized_end=8173
  _globals['_STATIONROUTE']._serialized_start=8176
  _globals['_STATIONROUTE']._serialized_end=8313
  _globals['_ROUTEWAYINFO']._serialized_start=8315
  _globals['_ROUTEWAYINFO']._serialized_end=8437
  _globals['_ROUTEWAYINFO_PAYLOAD']._serialized_start=8393
  _globals['_ROUTEWAYINFO_PAYLOAD']._serialized_end=8437
  _globals['_ROUTEWAYREPORT']._serialized_start=8439
  _globals['_ROUTEWAYREPORT']._serialized_end=8547
  _globals['_ROUTEWAYREPORT_PAYLOAD']._serialized_start=1658
  _globals['_ROUTEWAYREPORT_PAYLOAD']._serialized_end=1684
  _globals['_CARCONFIG']._serialized_start=8549
  _globals['_CARCONFIG']._serialized_end=8665
  _globals['_CARCONFIG_PAYLOAD']._serialized_start=8621
  _globals['_CARCONFIG_PAYLOAD']._serialized_end=8665
  _globals['_STATECHANGE']._serialized_start=8668
  _globals['_STATECHANGE']._serialized_end=8798
  _globals['_STATECHANGE_PAYLOAD']._serialized_start=8744
  _globals['_STATECHANGE_PAYLOAD']._serialized_end=8798
  _globals['_ECDSTATE']._serialized_start=8801
  _globals['_ECDSTATE']._serialized_end=9007
  _globals['_ECDSTATE_PAYLOAD']._serialized_start=8872
  _globals['_ECDSTATE_PAYLOAD']._serialized_end=9007
  _globals['_ECDSTATE_PAYLOAD_SINGLECABINET']._serialized_start=8938
  _globals['_ECDSTATE_PAYLOAD_SINGLECABINET']._serialized_end=9007
  _globals['_CABINETCONTROL']._serialized_start=9010
  _globals['_CABINETCONTROL']._serialized_end=9285
  _globals['_CABINETCONTROL_PAYLOAD']._serialized_start=9093
  _globals['_CABINETCONTROL_PAYLOAD']._serialized_end=9285
  _globals['_CABINETSTATE']._serialized_start=9288
  _globals['_CABINETSTATE']._serialized_end=9701
  _globals['_CABINETSTATE_ELECTRICDOOROBJECT']._serialized_start=9366
  _globals['_CABINETSTATE_ELECTRICDOOROBJECT']._serialized_end=9445
  _globals['_CABINETSTATE_ROLLERDOOROBJECT']._serialized_start=9447
  _globals['_CABINETSTATE_ROLLERDOOROBJECT']._serialized_end=9503
  _globals['_CABINETSTATE_PAYLOAD']._serialized_start=9506
  _globals['_CABINETSTATE_PAYLOAD']._serialized_end=9701
  _globals['_TRANSPORTCONTROL']._serialized_start=9704
  _globals['_TRANSPORTCONTROL']._serialized_end=9886
  _globals['_TRANSPORTCONTROL_PAYLOAD']._serialized_start=9790
  _globals['_TRANSPORTCONTROL_PAYLOAD']._serialized_end=9886
  _globals['_TRANSPORTCONTROLRESP']._serialized_start=9889
  _globals['_TRANSPORTCONTROLRESP']._serialized_end=10099
  _globals['_TRANSPORTCONTROLRESP_PAYLOAD']._serialized_start=9983
  _globals['_TRANSPORTCONTROLRESP_PAYLOAD']._serialized_end=10099
  _globals['_SELFCHECKREPORT']._serialized_start=10102
  _globals['_SELFCHECKREPORT']._serialized_end=10601
  _globals['_SELFCHECKREPORT_PAYLOAD']._serialized_start=10187
  _globals['_SELFCHECKREPORT_PAYLOAD']._serialized_end=10601
  _globals['_SELFCHECKREPORT_PAYLOAD_UNIFIEDERRORCODE']._serialized_start=10543
  _globals['_SELFCHECKREPORT_PAYLOAD_UNIFIEDERRORCODE']._serialized_end=10601
  _globals['_OPERATIONRESP']._serialized_start=10604
  _globals['_OPERATIONRESP']._serialized_end=10832
  _globals['_OPERATIONRESP_PAYLOAD']._serialized_start=10685
  _globals['_OPERATIONRESP_PAYLOAD']._serialized_end=10832
  _globals['_TASKEVENT']._serialized_start=10835
  _globals['_TASKEVENT']._serialized_end=10981
  _globals['_TASKEVENT_PAYLOAD']._serialized_start=10907
  _globals['_TASKEVENT_PAYLOAD']._serialized_end=10981
  _globals['_SYNCTASK']._serialized_start=10984
  _globals['_SYNCTASK']._serialized_end=11310
  _globals['_SYNCTASK_SUBTASK']._serialized_start=11054
  _globals['_SYNCTASK_SUBTASK']._serialized_end=11148
  _globals['_SYNCTASK_PAYLOAD']._serialized_start=11151
  _globals['_SYNCTASK_PAYLOAD']._serialized_end=11310
# @@protoc_insertion_point(module_scope)
