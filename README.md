# art-to-music

Quick start for GUI users
>
>
>

Quick start for Camera users
>
>
>

## Install

- ffmpeg: [click here](https://phoenixnap.com/kb/ffmpeg-windows) for windows or `apt install ffmpeg` for Ubuntu

### building dawdreamer for arm

As per June 8 we found out that a certain module called `dawdreamer` has no arm build, and since the target deploy is the Nvidea Jetson. This is [a discussion that you can track here](https://github.com/DBraun/DawDreamer/discussions/168)  

> 1. You will need to build [Juce](https://github.com/juce-framework/JUCE) for arm
by default it is not build for arm so `sudo apt install juce-tools`, did not work for me. *since that is a old verison or some other unknown magic*
Instead you want to `git clone https://github.com/juce-framework/JUCE.git` somewhere. I did it in my downloads folder.
go to `~/Downloads/JUCE/extras/Projucer/Builds/LinuxMakefile` and then run `make`
now you get the Projucer app, but you need to cp it into your `/usr/bin/` with: `cp `wherever the Projucer is` /usr/bin/Projucer`
Now if you run from your home `Projucer` it will start up
>  
> 2. Follow [these directives](https://github.com/DBraun/DawDreamer/discussions/168#discussioncomment-6039292), but in `Projucer /DawDreamer/DawDreamer.jucer` you also need to remove the `faustwithllvm` from `External Libraries to Link` for Linux Makefile  
![Screenshot from 2023-06-06 12-46-38](https://github.com/DBraun/DawDreamer/assets/103452406/81a74e35-ef5c-45ec-89a8-adf2ef1171a0)
>
> 3. and also i ran into a missing python.h error, but after i added the following on the top of my `/DawDreamer/build_linux.sh` it was fine
> ```sh
> PYTHONLIBPATH="/usr/lib/python3.10"
> PYTHONINCLUDEPATH="/usr/include/python3.10"
> ```
> What i think happened is:
> You need to run  `sudo sh build_linux.sh`, because `sudo` is required for `apt` and some other, but because it is `sudo` my external set variables where gone???
> So when you define it in the top of the sh script it is fine!
