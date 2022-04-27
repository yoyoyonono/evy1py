import mido
from util import *

mid = mido.MidiFile(midifilename := choose_midi_file_with_dragdrop())
newMid = mido.MidiFile(type=0)
newMid.add_track()
tempo = 1
for x in mid:
    x = x.copy()
    if x.is_meta and x.type == 'set_tempo':
        tempo = x.tempo//1
        print(tempo)
    x.time = round(mido.second2tick(x.time, mid.ticks_per_beat, tempo))
    x = normal_to_evy1(x)
    if not x.type == 'end_of_track' or not (not x.is_meta and x.channel == 9 and x.type == 'program_change'):
        newMid.tracks[0].append(x)

newMid.tracks[0].append(mido.MetaMessage('end_of_track'))
newMid.save("./out.mid")
with open("./out.mid", 'rb') as f:
    array = bytearray(f.read())

if len(array) > 32000:
    array = array[:32000]
else:
    array = array + bytearray(32000 - len(array))

out = ''
count = 0
for i in array:
    if count % 16 == 0:
        out += '\n'
    out += '0x{:02x}, '.format(i)
    count += 1
out = out[1:]

outfile = """
#include <TimerOne.h>
#include <avr/pgmspace.h> 

int led = 13;
unsigned long read_ptr;
unsigned long tempo;
unsigned long delta_time;
unsigned long tick_count;
unsigned char STATUS;
unsigned long TIMER;
int STATE;
int song = 0;


const unsigned char SMF_ROM[][32000] PROGMEM  = {
  {
""" + out + """
  },
};
  

void disable_timer( void )
{
  Timer1.stop();
}
void NSX1_MIDI_WRITE(unsigned char* buf , int num ){
  int i;
  for(i=0;i<num;i++){
   Serial.write(buf[i]);
/*
    Serial.print(buf[i],HEX) ; 
    Serial.print(" ") ;
*/
  }  
//  Serial.print("\\n") ;
}
unsigned char midi_read(void){
  unsigned char myChar;
    myChar =  pgm_read_byte_near(SMF_ROM[song] + read_ptr); // 
    read_ptr++;
  return myChar;
}

unsigned int delta_time_read(void){
  unsigned char  r_buf;
  unsigned int ret = 0;
  while(1){
    r_buf = midi_read();
    ret = (ret <<7) | (r_buf & 0x7f);
    if((r_buf & 0x80) == 0) break;
  }


  TIMER += (ret * tempo / delta_time);
  /*
  Serial.print("delta=");
   Serial.print(ret,DEC) ; Serial.print("\n") ;
   Serial.print(tempo,DEC) ; Serial.print("\n") ;
   Serial.print(delta_time,DEC) ; Serial.print("\n") ;
   Serial.print("TIMER=") ;
   Serial.print(TIMER,2) ; Serial.print("\n") ;
   */
  return ret;
}
void midi_play(void){
  unsigned char buf[256];
  int i = 2;
  int cnt ;
  buf[0] = midi_read();
  if(buf[0] & 0x80){
    STATUS = buf[0];
    buf[1] = midi_read();
  }
  else{
    buf[1] = buf[0];
    buf[0] = STATUS;
  }

  if((STATUS & 0xf0) == 0x80){
    buf[2] = midi_read();
    NSX1_MIDI_WRITE(&buf[0] ,3);
  }
  else if((STATUS & 0xf0) == 0x90){
    buf[2] = midi_read();
    NSX1_MIDI_WRITE(&buf[0] ,3);
  }
  else if((STATUS & 0xf0) == 0xA0){
    buf[2] = midi_read();
    NSX1_MIDI_WRITE(&buf[0] ,3);
  }
  else if((STATUS & 0xf0) == 0xB0){
    buf[2] = midi_read();
    NSX1_MIDI_WRITE(&buf[0] ,3);
  }
  else if((STATUS & 0xf0) == 0xC0){
    NSX1_MIDI_WRITE(&buf[0] ,2);
  }
  else if((STATUS & 0xf0) == 0xD0){
    NSX1_MIDI_WRITE(&buf[0] ,2);
  }
  else if((STATUS & 0xf0) == 0xE0){
    buf[2] = midi_read();
    NSX1_MIDI_WRITE(&buf[0] ,3);
  }
  else if((STATUS & 0xf0) == 0xF0){
    switch(	STATUS & 0x0f ){
    case 0x00 : //sysex
    case 0x07 : //Sysex2
      cnt = buf[1];
      for(i=1;i<cnt+1;i++){
        buf[i] = midi_read();
      }
      NSX1_MIDI_WRITE(&buf[0] ,cnt +1);
      break;
    case 0x0f:
      switch ( buf[1] ){
      case 0x51: //tempo
        midi_read(); // len
        tempo = midi_read();
        tempo = (tempo << 8 ) | midi_read();
        tempo = (tempo << 8 ) | midi_read();
        tempo = tempo / 1000 ;
        break;
      case 0x2f:
        midi_read(); // len
        disable_timer();
        STATE = 2;
        break;
      default:
        cnt = midi_read(); // len
        for(i=0;i<cnt;i++) midi_read();
        break;
      }
      break;
    }
  }
}



void smf_main_loop(void){
  int  file_count;
  if(STATE == 1){
    if(TIMER < tick_count){
      midi_play();
      file_count = delta_time_read();
    }
    if (read_ptr > sizeof(SMF_ROM[song])) {
      digitalWrite(52, LOW);
      delay(10);
      digitalWrite(52, HIGH);
    }
  }
}

void smf_init(void){
  TIMER = 0;
  tick_count = 0;
  STATUS = 0x00;
  tempo = 0x07A120 ;//tempo = 120
  tempo = tempo / 1000 ;
  //format 0 only
  read_ptr = 0x0c;
  //delta_time_read
  delta_time = (midi_read() << 8) | midi_read();
  //first delta time
  read_ptr = 0x16;
  TIMER = delta_time_read() * tempo / delta_time ;
  STATE = 1;
}
int k;
void timerIsr()
{
  // Toggle LED
  digitalWrite( 13, digitalRead( 13 ) ^ 1 );
  tick_count += 10;
  
    unsigned char myChar;
    // Toggle LED
    digitalWrite( 13, digitalRead( 13 ) ^ 1 );
    /*
    myChar =  pgm_read_byte_near(SMF_ROM[song] + k); // send 1 byte
    k++;
    Serial.print(myChar,HEX) ; 
    Serial.print(" ") ;
    if(k%16==0)Serial.print("\n") ;
    */
}                    

void setup() {  
  // initialize the digital pin as an output.
  digitalWrite(52, HIGH);
  pinMode(led, OUTPUT);  
  pinMode(52, OUTPUT);
  delay(4000);    // Wait a second for booting eVY1-Shleld.

  Timer1.initialize(10000); // set a timer of length 100000 microseconds (or 0.1 sec - or 10Hz => the led will blink 5 times, 5 cycles of on-and-off, per second)
  Timer1.attachInterrupt( timerIsr ); // attach the service routine here
  //  Set MIDI baud rate:
   Serial.begin(31250);
//  Serial.begin(38400);
  smf_init();


}

void loop() {

  smf_main_loop();  

}
"""

with open(f'{midifilename[:-4]}.ino', 'w') as f:
    f.write(outfile)