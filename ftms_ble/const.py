# fmt: off
from enum import IntEnum, IntFlag

FTMS_FITNESS_MACHINE_FEATURE_CHARACTERISTIC_UUID = "00002acc-0000-1000-8000-00805f9b34fb"
FTMS_FITNESS_MACHINE_STATUS_CHARACTERISTIC_UUID = "00002ada-0000-1000-8000-00805f9b34fb"
FTMS_TRAINING_STATUS_CHARACTERISTIC_UUID = "00002ad3-0000-1000-8000-00805f9b34fb"
FTMS_FITNESS_MACHINE_CONTROL_POINT_CHARACTERISTIC_UUID = "00002ad9-0000-1000-8000-00805f9b34fb"


class FitnessMachineFeature(IntFlag):
    """
    FTMS v1.0 section 4.3.1.1, Table 4.3
    """
    AVERAGE_SPEED =                                       0b00000001
    CADENCE =                                             0b00000010
    TOTAL_DISTANCE =                                      0b00000100
    INCLINATION =                                         0b00001000
    ELEVATION_GAIN =                                      0b00010000
    PACE =                                                0b00100000
    STEP_COUNT =                                          0b01000000
    RESISTANCE_LEVEL =                                    0b10000000
    STRIDE_COUNT =                               0b00000001_00000000
    EXPENDED_ENERGY =                            0b00000010_00000000
    HEART_RATE_MEASUREMENT =                     0b00000100_00000000
    METABOLIC_EQUIVALENT =                       0b00001000_00000000
    ELAPSED_TIME =                               0b00010000_00000000
    REMAINING_TIME =                             0b00100000_00000000
    POWER_MEASUREMENT =                          0b01000000_00000000
    FORCE_ON_BELT_AND_POWER_OUTPUT =             0b10000000_00000000
    USER_DATA_RETENTION =               0b00000001_00000000_00000000


class FitnessMachineTargetSettingFeature(IntFlag):
    """
    FTMS v1.0 section 4.3.1.2, Table 4.4
    """
    SPEED_TARGET_SETTING =                                                        0b00000001
    INCLINATION_SETTING_TARGET =                                                  0b00000010
    RESISTANCE_SETTING_TARGET =                                                   0b00000100
    POWER_SETTING_TARGET =                                                        0b00001000
    HEART_RATE_SETTING_TARGET =                                                   0b00010000
    TARGETED_EXPENDED_ENERGY_CONFIGURATION =                                      0b00100000
    TARGETED_STEP_NUMBER_CONFIGURATION =                                          0b01000000
    TARGETED_STRIDE_NUMBER_CONFIGURATION =                                        0b10000000
    TARGETED_DISTANCE_CONFIGURATION =                                    0b00000001_00000000
    TARGETED_TRAINING_TIME =                                             0b00000010_00000000
    TARGETED_TIME_IN_TWO_HEART_RATE_ZONES_CONFIGURATION =                0b00000100_00000000
    TARGETED_TIME_IN_THREE_HEART_RATE_ZONES_CONFIGURATION =              0b00001000_00000000
    TARGETED_TIME_IN_FIVE_HEART_RATE_ZONES_CONFIGURATION =               0b00010000_00000000
    INDOOR_BIKE_SIMULATION_PARAMETERS =                                  0b00100000_00000000
    WHEEL_CIRCUMFERENCE_CONFIGURATION =                                  0b01000000_00000000
    SPIN_DOWN_CONTROL =                                                  0b10000000_00000000
    TARGETED_CADENCE_CONFIGURATION =                            0b00000001_00000000_00000000


class FitnessMachineControlPointOperation(IntEnum):
    """
    FTMS v1.0 section 4.16.1, Table 4.15
    """
    REQUEST_CONTROL =                               0x00
    RESET =                                         0x01
    SET_TARGET_SPEED =                              0x02
    SET_TARGET_INCLINATION =                        0x03
    SET_TARGET_RESISTANCE_LEVEL =                   0x04
    SET_TARGET_POWER =                              0x05
    SET_TARGET_HEART_RATE =                         0x06
    START_OR_RESUME =                               0x07
    STOP_OR_PAUSE =                                 0x08
    SET_TARGETED_EXPENDED_ENERGY =                  0x09
    SET_TARGETED_NUMBER_OF_STEPS =                  0x0A
    SET_TARGETED_NUMBER_OF_STRIDES =                0x0B
    SET_TARGETED_DISTANCE =                         0x0C
    SET_TARGETED_TRAINING_TIME =                    0x0D
    SET_TARGETED_TIME_IN_TWO_HEART_RATE_ZONES =     0x0E
    SET_TARGETED_TIME_IN_THREE_HEART_RATE_ZONES =   0x0F
    SET_TARGETED_TIME_IN_FIVE_HEART_RATE_ZONES =    0x10
    SET_INDOOR_BIKE_SIMULATION_PARAMETERS =         0x11
    SET_WHEEL_CIRCUMFERENCE =                       0x12
    SPIN_DOWN_CONTROL =                             0x13
    SET_TARGETED_CADENCE =                          0x14

    RESPONSE_CODE =                                 0x80


class FitnessMachineStopCode(IntEnum):
    """
    FTMS v1.0 section 4.16.2.9, Table 4.16
    """
    STOP =  0x01
    PAUSE = 0x02


class FitnessMachineControlPointResponse(IntEnum):
    """
    FTMS v1.0 section 4.16.2.22, Table 4.24
    """
    SUCCESS =                   0x01
    OPERATION_NOT_SUPPORTED =   0x02
    INVALID_PARAMETER =         0x03
    OPERATION_FAILED =          0x04
    CONTROL_NOT_PERMITTED =     0x05


class FitnessMachineStatusCode(IntEnum):
    """
    FTMS v1.0 section 4.17, Table 4.26
    """
    RESET =                                     0x01
    STOPPED_OR_PAUSED_BY_USER =                 0x02
    STOPPED_BY_SAFETY_KEY =                     0x03
    STARTED_OR_RESUMED_BY_USER =                0x04
    TARGET_SPEED_CHANGED =                      0x05
    TARGET_INCLINE_CHANGED =                    0x06
    TARGET_RESISTANCE_LEVEL_CHANGED =           0x07
    TARGET_POWER_CHANGED =                      0x08
    TARGET_HEART_RATE_CHANGED =                 0x09
    TARGET_EXPENDED_ENERGY_CHANGED =            0x0A
    TARGET_NUMBER_OF_STEPS_CHANGED =            0x0B
    TARGET_NUMBER_OF_STRIDES_CHANGED =          0x0C
    TARGET_DISTANCE_CHANGED =                   0x0D
    TARGET_TRAINING_TIME_CHANGED =              0x0E
    TARGET_TIME_IN_TWO_HEART_RATE_ZONES =       0x0F
    TARGET_TIME_IN_THREE_HEART_RATE_ZONES =     0x10
    TARGET_TIME_IN_FIVE_HEART_RATE_ZONES =      0x11
    INDOOR_BIKE_SIMULATION_PARAMETERS_CHANGED = 0x12
    WHEEL_CIRCUMFERENCE_CHANGED =               0x13
    SPIN_DOWN_STATUS =                          0x14
    TARGETED_CADENCE_CHANGED =                  0x15

    CONTROL_PERMISSION_LOST =                   0xFF
