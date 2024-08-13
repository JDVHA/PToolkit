#include "MCOM.h"

MCOM::MCOM(int numcommands)
{
  L = new command[numcommands];
  commandcount = numcommands;
}

void MCOM::Start()
{
  Serial.println("Starting...");
  Serial.println("MCOM has started.");
}

void MCOM::HandleInput()
{
  while (Serial.available())
  {
    incomingstring = Serial.readString();
    incomingstring.trim();
    Serial.print("Received: ");
    Serial.println(incomingstring);
    this->MCOM::Handlecommand(incomingstring);
  }
}

void MCOM::Handlecommand(String incomingstring)
{
  if (incomingstring == "list")
  {
    this->MCOM::Listallcommands();
  }
  else
  {
    for (int i = 0; i < commandcount; i++)
    {
      if (L[i].str == incomingstring)
      {
        String output = (*L[i].ptr)();
        Serial.println(output);
        break;
      }
      else if (i + 1 < commandcount)
      {
        Serial.println("Unkown command: " + incomingstring);
      }
    }
  }
}

void MCOM::Listallcommands()
{
  Serial.println("Available commands:");
  for (int i = 0; i < commandcount; i++)
  {
    Serial.println("\t- " + L[i].str);
  }
}

void MCOM::Addcommand(String cname, String (*func)())
{
  L[currentcommand].str = cname;
  L[currentcommand].ptr = func;
  currentcommand++;
};
