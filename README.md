# synchCams
Toolbox for synchronized dual camera acquisition

synchCams is a library for the acquisition of synchronized dual camera video. The videos are saved with alternate acquisition of frames. This ensures equal number of frames. 

## Features
- synchCams can be used standalone or as a library. 
- saves timestamps of frames acquired and a lot of other experimental details
- can be integrated with serial triggers (can wait for and send triggers to a serial port)

## Installation
Install the library using:
```bash
pip install synchCams
```

## In Development
synchCams can also be used using parallel processing (interleaved frames are not guaranteed)


## License
The MIT License (MIT)
Copyright 2021 <Atesh Koul>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.