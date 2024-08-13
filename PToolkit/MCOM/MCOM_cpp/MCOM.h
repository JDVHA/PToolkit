#ifndef MCOM_H
#define MCOM_H

#include <Arduino.h>


typedef struct command{
  String str;
  String (*ptr)();
};

class MCOM{
 public:
    String incomingstring;
    command *L;
    int commandcount;
    int currentcommand = 0;

    MCOM(int numcommands);
};

#endif
