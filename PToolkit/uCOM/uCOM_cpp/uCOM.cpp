#include "uCom.h"

uCom::uCom(int nuuCommands)
{
  L = new command[nuuCommands];
  commandcount = nuuCommands;
}

void uCom::Start()
{
  Serial.println("Starting...");
  Serial.println("uCom has started.");
}

void uCom::HandleInput()
{
  while (Serial.available())
  {
    incomingstring = Serial.readString();
    incomingstring.trim();
    Serial.print("Received: ");
    Serial.println(incomingstring);
    this->uCom::Handlecommand(incomingstring);
  }
}

void uCom::Handlecommand(String incomingstring)
{
  if (incomingstring == "list")
  {
    this->uCom::Listallcommands();
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

void uCom::Listallcommands()
{
  Serial.println("Available commands:");
  for (int i = 0; i < commandcount; i++)
  {
    Serial.println("\t- " + L[i].str);
  }
}

void uCom::Addcommand(String cname, String (*func)())
{
  L[currentcommand].str = cname;
  L[currentcommand].ptr = func;
  currentcommand++;
};
