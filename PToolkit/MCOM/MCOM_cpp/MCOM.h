#ifndef MCOM_H
#define MCOM_H

#include <Arduino.h>

typedef struct command
{
  String str;
  String (*ptr)();
};

class MCOM
{
public:
  String incomingstring;
  command *L;
  int commandcount;
  int currentcommand = 0;
  MCOM(int numcommands);
  void Start();
  void HandleInput();
  void Handlecommand(String incomingstring);
  void Listallcommands();
  void Addcommand(String cname, String (*func)());
};

#endif
