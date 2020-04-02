#include "winrt/base.h"

#include <cstdlib>
#include <iostream>


int main()
{
    std::cout << CPPWINRT_VERSION << std::endl;

    winrt::init_apartment();

    return EXIT_SUCCESS;
}
