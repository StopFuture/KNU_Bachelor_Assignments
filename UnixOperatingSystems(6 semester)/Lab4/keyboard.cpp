//
// Created by Fedorych Andriy on 20/4/24.
//
#include <iostream>
#include <IOKit/IOKitLib.h>
#include <IOKit/hid/IOHIDManager.h>
static void keyboardEventCallback(void* context, IOReturn result, void* sender, IOHIDValueRef value) {
    if (result != kIOReturnSuccess) {
        std::cerr << "Keyboard event error: " << result << std::endl;
        return;
    }

    IOHIDElementRef element = IOHIDValueGetElement(value);
    if (!element) {
        std::cerr << "Invalid keyboard event element." << std::endl;
        return;
    }

    CFStringRef elementName = IOHIDElementGetName(element);
    if (!elementName) {
        std::cerr << "Failed to get keyboard event element name." << std::endl;
        return;
    }

    CFIndex usage = IOHIDElementGetUsage(element);
    CFIndex value64 = IOHIDValueGetIntegerValue(value);

    std::cout << "Keyboard event: " << CFStringGetCStringPtr(elementName, kCFStringEncodingUTF8)
              << " (Usage: " << usage << ", Value: " << value64 << ")" << std::endl;

    CFRelease(elementName);
}

int main() {
    // Create an HID manager object
    IOHIDManagerRef hidManager = IOHIDManagerCreate(kCFAllocatorDefault, kIOHIDOptionsTypeNone);
    if (!hidManager) {
        std::cerr << "Failed to create HID manager." << std::endl;
        return EXIT_FAILURE;
    }

    // Open the HID manager
    IOReturn openStatus = IOHIDManagerOpen(hidManager, kIOHIDOptionsTypeNone);
    if (openStatus != kIOReturnSuccess) {
        std::cerr << "Failed to open HID manager. Error: " << openStatus << std::endl;
        CFRelease(hidManager);
        return EXIT_FAILURE;
    }

    // Set up a callback to handle keyboard events
    IOHIDManagerRegisterInputValueCallback(hidManager, keyboardEventCallback, nullptr);

    // Start the HID manager
    IOHIDManagerScheduleWithRunLoop(hidManager, CFRunLoopGetCurrent(), kCFRunLoopDefaultMode);

    // Run the event loop
    CFRunLoopRun();

    // Clean up
    IOHIDManagerUnscheduleFromRunLoop(hidManager, CFRunLoopGetCurrent(), kCFRunLoopDefaultMode);
    CFRelease(hidManager);

    return EXIT_SUCCESS;
}

