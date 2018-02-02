#include <iostream>
#include <limits>

int main(void) {
  std::cout << std::numeric_limits<double>::min() << ", " << 
               std::numeric_limits<double>::max() << ", " <<
               - std::numeric_limits<double>::max() << std::endl;
  return 0;
}

