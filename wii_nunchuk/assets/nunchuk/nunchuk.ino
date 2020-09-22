/*
 * Weitere Infos: www.makerblog.at
 * 
 * Library zum Download: https://github.com/timtro/wiinunchuck-h
 * Achtung: Nach dem Download des ZIPs und vor dem Import der Library in die Arduino IDE
 * das "-master" aus dem Dateinamen löschen.
 */
 
#include <Wire.h>
#include <wiinunchuck.h>
 
void setup() {
 
  Serial.begin(115200);
 
  // Nunchuk initialisieren und Joystick auf Mittelposition kalibrieren
  nunchuk_init();
  delay(100);
  nunchuk_calibrate_joy();
  delay(100);
}
 
void loop() {
 
  // Daten (6 Byte) vom Nunchuk Controller auslesen
  nunchuk_get_data();
  // Die einzelnen Werte stehen jetzt in Funktionen der WiiNunchuck-Library zur Verfügung
 
  char buffer[36];
  /* 
   *  sprintf() wird dazu verwendet, um einen String aus einem formatierten Vorlagenstring zu erzeugen. 
   *  Hierfür wird in den Buffer, der als erstes Argument erzeugt wird der Formatstring kopiert 
   *  und die Substitutionszeichen werden mit den gegebenen Parametern ersetzt. 
   *  %3d bedeutet z.B.: Formatiere immer 3-stellig, notfalls mit führenden Leerzeichen
   */
  sprintf(buffer, "%3d,%3d,%3d,%3d,%3d,%3d,%3d,%3d,%1d,%1d", 
    nunchuk_accelx(), 
    nunchuk_accely(), 
    nunchuk_accelz(), 
    nunchuk_caccelx(), 
    nunchuk_caccely(), 
    nunchuk_caccelz(),
    nunchuk_cjoy_x(),
    nunchuk_cjoy_y(), 
    nunchuk_zbutton(), 
    nunchuk_cbutton());
 
  // Zusammengesetzten String an den seriellen Monitor schicken
  Serial.println(buffer);
 
  delay(1);
}
