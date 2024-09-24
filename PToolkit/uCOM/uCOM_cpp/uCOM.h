#ifndef uCom_H
#define uCom_H

#include <Arduino.h>

typedef struct command
{
  String str;
  String (*ptr)();
};

class uCom
{
public:
  String incomingstring;
  command *L;
  int commandcount;
  int currentcommand = 0;
  uCom(int nuuCommands);
  void Start();
  void HandleInput();
  void Handlecommand(String incomingstring);
  void Listallcommands();
  void Addcommand(String cname, String (*func)());
};

#endif
