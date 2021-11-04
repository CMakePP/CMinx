.. Copyright 2021 CMakePP
..
.. Licensed under the Apache License, Version 2.0 (the "License");
.. you may not use this file except in compliance with the License.
.. You may obtain a copy of the License at
..
.. http://www.apache.org/licenses/LICENSE-2.0
..
.. Unless required by applicable law or agreed to in writing, software
.. distributed under the License is distributed on an "AS IS" BASIS,
.. WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
.. See the License for the specific language governing permissions and
.. limitations under the License.
..

#######################
advanced_function.cmake
#######################

.. module:: advanced_function.cmake


.. function:: advanced_say_hi_to(me)
   
   Variation of say_hi_to, which takes lists of people and cats to say hi to.
   
   This function is basically the same as ``say_hi_to``, but accounts for the
   fact that you may want to say hi to multiple people and maybe even a cat or
   two.
   
   :param me: The name of the person saying hi.
   :type me: string
   :keyword PERSONS: The person or persons to say hi to.
   :type PERSONS: list of strings
   :keyword CATS: The cat or cats to say hi to.
   :type CATS: list of strings
   

