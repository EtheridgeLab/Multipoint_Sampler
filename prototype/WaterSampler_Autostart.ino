// Enter number of valves to be used:
const int valveMax = 4;

// *****Use tubing of 75ft. length or less*****  -> spectrometer delay does not allow enough time to draw completely through 100 ft. lengths.

// Enter length of line attached to Valve 1:
const int length1 = 25;

// Enter length of line attached to Valve 2:
const int length2 = 25;

// Enter length of line attached to Valve 3:
const int length3 = 50;

// Enter length of line attached to Valve 4:
const int length4 = 75;

// Enter length of line attached to Valve 5:
const int length5 = 0;

// Enter length of line attached to Valve 6:
const int length6 = 0;


// *****************ENSURE THAT THE SPECTROMETER DELAY IS SET TO 250 SECONDS****************************************

//-----------------------------------------------------------------------------------------------------------------------------------------------------------

const int forward = 3;          // Runs pump forward/prime
const int reverse = 2;          // Runs pump in reverse/purge
const int scan = 13;            // Input signal from s::can computer
const int cycleTime = 10000;     // Duration of time pause during scan
const int signalTime = 1500;    // Duration of s::can signal required to progress cycle -- subtract 1000ms from intended duration for processing time
int inputMode = 0;              // Stores input state from s::can computer. 0 is "off", 1 is "on".
int count = 1;                  // Tracks number of pump/purge cycles. Used to determine which valve is open per cycle.
int countMax;                   // The number of valves to be used for a testing cycle; limits loop to include only used valves
int valve;                      // Represents specific valves based on cycle count
long prepTime;                  // Represents water line prime/purge time duration based on cycle count
long timeBalance;               // Used to increase duration of cycleTime - adds difference of 250 seconds and prepTime

// Designates valves to corresponding input pins
const int valve1 = 12;          
const int valve2 = 11;         
const int valve3 = 10;          
const int valve4 = 9;           
const int valve5 = 8;           
const int valve6 = 7;     

// The duration of time to prep (prime/purge) the water line associated with
// each valve. Determined by function setTime.
long prepTime1;                  
long prepTime2;
long prepTime3;
long prepTime4;
long prepTime5;
long prepTime6;


void setup() { 

  Serial.begin(9600);
  pinMode(forward, OUTPUT);
  pinMode(reverse, OUTPUT);
  pinMode(valve1, OUTPUT);
  pinMode(valve2, OUTPUT);
  pinMode(valve3, OUTPUT);
  pinMode(valve4, OUTPUT);
  pinMode(valve5, OUTPUT);
  pinMode(valve6, OUTPUT);
  pinMode(scan, INPUT);          // Receives signal from s::can computer

  digitalWrite(valve1, LOW);
  digitalWrite(valve2, LOW);
  digitalWrite(valve3, LOW);
  digitalWrite(valve4, LOW);
  digitalWrite(valve5, LOW);
  digitalWrite(valve6, LOW);
}

void loop(){
  
  // Sets up int "valve" to be used in place of individual valves.
  // Allows single routine to control operation of all valves.
  // Exits routine if count exceeds number of usable valves.
  if(count==1){valve=valve1; prepTime=setTime(length1);}
  else if(count==2){valve=valve2; prepTime=setTime(length2);}
  else if(count==3){valve=valve3; prepTime=setTime(length3);}
  else if(count==4){valve=valve4; prepTime=setTime(length4);}
  else if(count==5){valve=valve5; prepTime=setTime(length5);}
  else if(count==6){valve=valve6; prepTime=setTime(length6);}
  timeBalance = 250000 - prepTime;

  // Display how many input lines are connected, which input line is currently in use, how long the pump will run, and the delay between pump shut-off and spectrometer scan
  Serial.print("Number of valves used: ");
  Serial.println(valveMax);
  Serial.print("Valve in use: ");
  Serial.println(count);
  Serial.print("Prime duration: ");
  Serial.print(prepTime/1000);
  Serial.println(" seconds");
  Serial.print("Time offset is: ");
  Serial.print(timeBalance/1000);
  Serial.println(" seconds");

  Serial.println("\nWaiting for signal...\n");

  // Program will wait until s::can signal detected
  // Saves 0 or 1 to variable 'inputMode'
  // Requires function scanInput
  inputMode = scanInput();    
  
  //*****Functional routine*****
  //Valves closed on LOW, open on HIGH

  // When the trigger signal is detected (scanInput returns 1)
  if(inputMode==1){
    // Valve opens, 0.5-second delay, pump engages forward
    digitalWrite(valve, HIGH);
    Serial.print("Valve "); 
    Serial.print(count); 
    Serial.println(" is open.\n");
    delay(250);
    Serial.println("Priming...\n");
    digitalWrite(forward, HIGH);
    delay(prepTime);

    // Begin test cycle: valve stays open, pump stops for testing
    Serial.println("Testing...\n");
    digitalWrite(forward, LOW);
    digitalWrite(valve, LOW);
    delay(cycleTime+(250000-prepTime));

    // Purge open valve
    Serial.println("Purging...\n");
    digitalWrite(valve, HIGH);
    delay(250);
    digitalWrite(reverse,HIGH);
    delay(15000);                      // 15 seconds
    digitalWrite(reverse,LOW);
    delay(250);

    // Closes valve
    digitalWrite(valve,LOW);
    Serial.print("Valve ");
    Serial.print(count);
    Serial.println(" is closed.\n");

    // When cycle is complete: reset inputMode, increase count, (if last valve has ben used) return to first valve
    inputMode = 0;
    count++;
    if(count > valveMax){count = 1;}
  }
}


//********************FUNCTIONS********************

  // This function returns a time duration based on a distance entered by the user.
  // It does not requre require a variable when called by parent function. 
  // If  unput distance is less than 0 or greater than 100, the user will be prompted
  // with a message to reenter a value that falls within the range.
  // ENSURE THAT THE SPECTROMETER DELAY IS SET TO 250 SECONDS
  
long setTime(int duration){
  
  long millisecs;

  if((duration > 0) && (duration <= 25)){millisecs = 80000;}
  else if((duration > 25) && (duration < 50)){millisecs = 140000;}
  else if((duration >= 50) && (duration <= 75)){millisecs = 200000;}
  //else if((duration >= 75) && (duration <= 100)){millisecs = 250000;}  **Left in case smaller-diameter tubing is used and draw time decreases**
  return millisecs;
}

//--------------------------------------------------------------------------------------------------

  // Checks for signal input from S::CAN terminal
  // **Try using code chunk from previous code**
  
int scanInput(){
  here:
  int test = digitalRead(scan);
  if(test==HIGH){
    delay(signalTime);
    test = digitalRead(scan);
    if(test==HIGH){
      return 1;
      Serial.println("ok");
    }
  }
  goto here;
}
