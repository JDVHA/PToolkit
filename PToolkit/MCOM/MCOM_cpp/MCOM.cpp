#include "MCOM.h"
typedef struct command{
  String str;
  String (*ptr)();
};

class MCOM {
  public:
    String incomingstring;
    command *L;
    int commandcount;
    int currentcommand = 0;

    MCOM(int numcommands){
      L = new command[numcommands];
      commandcount = numcommands;
    }

    void Start(){
      Serial.println("Starting...");
      Serial.println("MCOM has started.");
    }

    void HandleInput() {
      while (Serial.available()){
        incomingstring = Serial.readString();
        incomingstring.trim();
        Serial.print("Received: ");
        Serial.println(incomingstring);
        this->MCOM::Handlecommand(incomingstring);
      }
    }

    void Handlecommand(String incomingstring){
      if (incomingstring == "list"){
            this->MCOM::Listallcommands();
            
          }
      else{
          for (int i = 0; i < commandcount; i++){
            if (L[i].str == incomingstring){
               String output = (*L[i].ptr)();
               Serial.println(output);
               break;
            }
            else if (i+1 < commandcount){
              Serial.println("Unkown command: " + incomingstring);
            }
        }
      }
      
    }

    void Listallcommands(){
      Serial.println("Available commands:");
      for (int i =0; i< commandcount; i++){
        Serial.println("\t- " + L[i].str);
      }
    }

    void Addcommand(String cname, String (*func)()){
      L[currentcommand].str = cname;
      L[currentcommand].ptr = func;
      currentcommand++;
      };
    
};
