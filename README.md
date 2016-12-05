

## Question types

`questions` is a list of questions. Each question has a type.

* list
* confirm


## Question values

A question is a dictionary containing question related values:

* type: (String) Type of the prompt. Defaults: input - Possible values: input, confirm, list, rawlist, expand, checkbox, password, editor
* name: (String) The name to use when storing the answer in the answers hash. If the name contains periods, it will define a path in the answers hash.
* message: (String|Function) The question to print. If defined as a function, the first parameter will be the current inquirer session answers.
* default: (String|Number|Array|Function) Default value(s) to use if nothing is entered, or a function that returns the default value(s). If defined as a function, the first parameter will be the current inquirer session answers.
* choices: (Array|Function) Choices array or a function returning a choices array. If defined as a function, the first parameter will be the current inquirer session answers. Array values can be simple strings, or objects containing a name (to display in list), a value (to save in the answers hash) and a short (to display after selection) properties. The choices array can also contain a Separator.
* validate: (Function) Receive the user input and should return true if the value is valid, and an error message (String) otherwise. If false is returned, a default error message is provided.
* filter: (Function) Receive the user input and return the filtered value to be used inside the program. The value returned will be added to the Answers hash.
* when: (Function, Boolean) Receive the current user answers hash and should return true or false depending on whether or not this question should be asked. The value can also be a simple boolean.
* pageSize: (Number) Change the number of lines that will be rendered when using list, rawList, expand or checkbox.





##Contributing

Unit test Unit test are written using pytest. Please add a unit test for every new feature or bug fix.

Documentation Add documentation for every API change. Feel free to send typo fixes and better docs!

We're looking to offer good support for multiple prompts and environments. If you want to help, we'd like to keep a list of testers for each terminal/OS so we can contact you and get feedback before release. Let us know if you want to be added to the list.


## About Windows support

prompt_toolkit is cross platform, and everything that you build on top should run fine on both Unix and Windows systems. On Windows, it uses a different event loop (WaitForMultipleObjects instead of select), and another input and output system. (Win32 APIs instead of pseudo-terminals and VT100.)

It's worth noting that the implementation is a "best effort of what is possible". Both Unix and Windows terminals have their limitations. But in general, the Unix experience will still be a little better.

For Windows, it's recommended to use either cmder or conemu.

## License

Copyright (c) 2016 Mark Fink (twitter: @markfink) Licensed under the MIT license.