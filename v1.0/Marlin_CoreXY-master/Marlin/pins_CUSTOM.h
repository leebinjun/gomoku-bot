/**
 * Arduino Mega with CUSTOM pin assignments
 *
 *
 *  Other pins_MYBOARD.h files may override these defaults
 */

#if !defined(__AVR_ATmega1280__) && !defined(__AVR_ATmega2560__)
  #error Oops!  Make sure you have 'Arduino Mega' selected from the 'Tools -> Boards' menu.
#endif

#define LARGE_FLASH true

#define X_STEP_PIN         16
#define X_DIR_PIN          17
#define X_ENABLE_PIN       -1
#define X_MIN_PIN          25
#define X_MAX_PIN          24

#define Y_STEP_PIN         18
#define Y_DIR_PIN          19
#define Y_ENABLE_PIN       -1
#define Y_MIN_PIN          27
#define Y_MAX_PIN          26

#define Z_STEP_PIN         20
#define Z_DIR_PIN          21
#define Z_ENABLE_PIN       -1
#define Z_MIN_PIN          28
#define Z_MAX_PIN          -1

#define Y2_STEP_PIN        -1
#define Y2_DIR_PIN         -1
#define Y2_ENABLE_PIN      -1

#define Z2_STEP_PIN        -1
#define Z2_DIR_PIN         -1
#define Z2_ENABLE_PIN      -1

#define E0_STEP_PIN        14
#define E0_DIR_PIN         15
#define E0_ENABLE_PIN      12 // NOT SOLDERED!

#define E1_STEP_PIN        -1
#define E1_DIR_PIN         -1
#define E1_ENABLE_PIN      -1

#define SDPOWER            -1
#define SDSS               53
#define LED_PIN            13

#define FILWIDTH_PIN       -1
#define FILRUNOUT_PIN      -1

#define FAN_PIN            3
#define CONTROLLERFAN_PIN  -1 // Pin used for the fan to cool controller

#define PS_ON_PIN          -1

#define KILL_PIN           -1

#define HEATER_0_PIN        2   // EXTRUDER 1

#define HEATER_1_PIN       -1

#define TEMP_0_PIN          0   // ANALOG NUMBERING
#define TEMP_1_PIN         -1   // ANALOG NUMBERING
#define TEMP_2_PIN         -1   // ANALOG NUMBERING

#define HEATER_BED_PIN      5    // BED

#define TEMP_BED_PIN        1   // ANALOG NUMBERING

#ifdef NUM_SERVOS
  #define SERVO0_PIN         29
  #if NUM_SERVOS > 1
    #define SERVO1_PIN        6
    #if NUM_SERVOS > 2
      #define SERVO2_PIN      5
      #if NUM_SERVOS > 3
        #define SERVO3_PIN    4
      #endif
    #endif
  #endif
#endif

#ifdef ULTRA_LCD

  #ifdef NEWPANEL
    #ifdef PANEL_ONE
      #define LCD_PINS_RS 40
      #define LCD_PINS_ENABLE 42
      #define LCD_PINS_D4 65
      #define LCD_PINS_D5 66
      #define LCD_PINS_D6 44
      #define LCD_PINS_D7 64
    #else
      #define LCD_PINS_RS 16
      #define LCD_PINS_ENABLE 17
      #define LCD_PINS_D4 23
      #define LCD_PINS_D5 25
      #define LCD_PINS_D6 27
      #define LCD_PINS_D7 29
    #endif


    #ifdef REPRAP_DISCOUNT_SMART_CONTROLLER
      #define BEEPER 37

      #define BTN_EN1 31
      #define BTN_EN2 33
      #define BTN_ENC 35

      #define SDCARDDETECT 49
    #elif defined(LCD_I2C_PANELOLU2)
      #define BTN_EN1 47  // reverse if the encoder turns the wrong way.
      #define BTN_EN2 43
      #define BTN_ENC 32
      #define LCD_SDSS 53
      #define SDCARDDETECT -1
      #define KILL_PIN 41
    #elif defined(LCD_I2C_VIKI)
      #define BTN_EN1 22  // reverse if the encoder turns the wrong way.
      #define BTN_EN2 7
      #define BTN_ENC -1
      #define LCD_SDSS 53
      #define SDCARDDETECT 49
    #else
      // arduino pin which triggers an piezzo beeper
      #define BEEPER 33  // Beeper on AUX-4

      // buttons are directly attached using AUX-2
      #ifdef REPRAPWORLD_KEYPAD
        #define BTN_EN1 64 // encoder
        #define BTN_EN2 59 // encoder
        #define BTN_ENC 63 // enter button
        #define SHIFT_OUT 40 // shift register
        #define SHIFT_CLK 44 // shift register
        #define SHIFT_LD 42 // shift register
      #elif defined(PANEL_ONE)
        #define BTN_EN1 59 // AUX2 PIN 3
        #define BTN_EN2 63 // AUX2 PIN 4
        #define BTN_ENC 49 // AUX3 PIN 7
      #else
        #define BTN_EN1 37
        #define BTN_EN2 35
        #define BTN_ENC 31  // the click
      #endif

      #ifdef G3D_PANEL
        #define SDCARDDETECT 49
      #else
        #define SDCARDDETECT -1  // Ramps does not use this port
      #endif

    #endif

  #else // Old-style panel with shift register
    // Arduino pin witch triggers an piezzo beeper
    #define BEEPER 33   // No Beeper added

    // Buttons are attached to a shift register
    // Not wired yet
    // #define SHIFT_CLK 38
    // #define SHIFT_LD 42
    // #define SHIFT_OUT 40
    // #define SHIFT_EN 17

    #define LCD_PINS_RS 16
    #define LCD_PINS_ENABLE 17
    #define LCD_PINS_D4 23
    #define LCD_PINS_D5 25
    #define LCD_PINS_D6 27
    #define LCD_PINS_D7 29
  #endif
#endif // ULTRA_LCD

// SPI for Max6675 Thermocouple
#ifndef SDSUPPORT
  #define MAX6675_SS       66 // Do not use pin 53 if there is even the remote possibility of using Display/SD card
#else
  #define MAX6675_SS       66 // Do not use pin 49 as this is tied to the switch inside the SD card socket to detect if there is an SD card present
#endif

#ifndef SDSUPPORT
  // these pins are defined in the SD library if building with SD support
  #define SCK_PIN          52
  #define MISO_PIN         50
  #define MOSI_PIN         51
#endif
