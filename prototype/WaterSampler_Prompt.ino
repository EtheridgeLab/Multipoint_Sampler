/*
 Created by Shawn Harbin, 2018
 for Dr. Randall Etheridge -- East Carolina University, Department of Engineering 

 This program controls 6 valves and peristaltic pump, initiated by S::CAN computer.

 For proper interface with Serial Monitor, ensure that option is set to "no line ending"
*/



const int forward = 3;          // Runs pump forward/prime
const int reverse = 2;          // Runs pump in reverse/purge
const int scan = 13;            // Input signal from s::can computer
const long cycleTime = 1000;    // Duration of time to run pump during scan
const long signalTime = 1500;   // Duration of s::can signal required to progress cycle -- subtract 1000ms from intended duration for processing time
int inputMode = 0;              // Stores input state from s::can computer. 0 is "off", 1 is "on".
int count = 1;                  // Tracks number of pump/purge cycles. Used to determine which valve is open per cycle.
int prepCount = 1;              // Tracks first cycle for each valve; maxes out at countMax+1
int valveMax;                   // The number of valves to be used for a testing cycle; limits loop to include only used valves
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

  Serial.println("\n**NOTICE**");
  Serial.println("Before continuing, please ensure that your serial monitor option is set to 'No line ending'.");
  Serial.println("Failure to do so will cause errors with pump prime and purge times. Thank you.\n");
  delay(2000);

  // User will be prompted to enter the number of inputs to be used. This will serve as the limit for number of 
  // cycles to be run before returning to the first input. Input is limited to 1-6; inputs less than 1 or greater
  // than 6 will prompt a message to re-enter a value within that range.
  here:
  Serial.print("Enter number of valves to be used: ");
  while(Serial.available()==0){}
  valveMax = Serial.parseInt();
  Serial.println(valveMax);
  if(valveMax<1 || valveMax>6){
    Serial.println("\n   ***Please enter a value between 1 and 6***\n");
    goto here;}
  
  Serial.println();

  // User will be prompted to input the lengths of tubing connected to each input, limited to the maximum number
  // of inputs used. These lengths will be used to determine priming duration for each line.
  // Requires function setTime
  if(valveMax>=1){
    Serial.println("What is the length (in ft.) of the water line connected to Valve 1?");
    prepTime1 = setTime();}
  if(valveMax>=2){
    Serial.println("What is the length (in ft.) of the water line connected to Valve 2?");
    prepTime2 = setTime();}
  if(valveMax>=3){
    Serial.println("What is the length (in ft.) of the water line connected to Valve 3?");
    prepTime3 = setTime();}
  if(valveMax>=4){
    Serial.println("What is the length (in ft.) of the water line connected to Valve 4?");
    prepTime4 = setTime();}
  if(valveMax>=5){
    Serial.println("What is the length (in ft.) of the water line connected to Valve 5?");
    prepTime5 = setTime();}
  if(valveMax>=6){
    Serial.println("What is the length (in ft.) of the water line connected to Valve 6?");
    prepTime6 = setTime();}

  delay(250);
  Serial.println("Beginning new data collection cycle.\n");
}

void loop(){

  // Sets up int "valve" to be used in place of individual valves.
  // Allows single routine to control operation of all valves.
  // Exits routine if count exceeds number of usable valves.
  if(count==1){valve=valve1; prepTime=prepTime1;}
  else if(count==2){valve=valve2; prepTime=prepTime2;}
  else if(count==3){valve=valve3; prepTime=prepTime3;}
  else if(count==4){valve=valve4; prepTime=prepTime4;}
  else if(count==5){valve=valve5; prepTime=prepTime5;}
  else if(count==6){valve=valve6; prepTime=prepTime6;}
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
    delay(cycleTime + timeBalance);

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
long setTime(){
  int userInput;
  long seconds;
  long millisecs;
  
  retry:
  while(Serial.available()==0){}
  userInput = Serial.parseInt();

  if((userInput > 0) && (userInput <= 25)){millisecs = 80000;}
  else if((userInput > 25) && (userInput < 50)){millisecs = 140000;}
  else if((userInput >= 50) && (userInput <= 75)){millisecs = 200000;}
  //else if((userInput >= 75) && (userInput <= 100)){millisecs = 250000;}
  else if((userInput > 75) || (userInput <= 0)){
    Serial.println("   Please enter a distance of 1 - 75 ft: ");
    goto retry;
  }
  seconds = millisecs / 1000;
  Serial.print("   Length is ");
  Serial.print(userInput);
  Serial.println(" ft.");
  Serial.print("   Line prime and purge times will be ");
  Serial.print(seconds);
  Serial.println(" secs.\n");
  return millisecs;
}

//--------------------------------------------------------------------------------------------------

int scanInput(){
  // Used to test HIGH input signal for duration
  // When HIGH input detected, duration is tested, and returns 1 if satisfied.
  // Main program will pause here until satisfactory signal is detected - nothing returned until then
  // Uses variable "signalTime" (defined in main program) to compare time against
  
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
