namespace Lab5_APT;
/// <summary>
/// Name: Aidan Trusky
/// Date: 10/13/25
/// Description: 
///       This lab is aimed at creating effective unit tests for a previous lab we completed. 
///       We are asked to create a number of tests that will tests edge cases and confirm that our code
///       is working correctly. 
/// Bugs:
///       I added the xaml files over by mistake, and that was causing issues because it was looking 
///       for other files I did not transition over. I then put a Console.Writeline statement in the database
///       class to see if it was working, but it just kept printing the same message everytime I wiped the slate
///       clean. I also had to make a case that checked if there was any leftover data in supabase from the 
///       app or previous tests, because my first tests wouldn't start unless the table was empty.
/// Reflection (including description of any LLM usage):
///       I think the part that look me the longest on this lab was thinking of all the edge cases to go through. 
///       Once I knew how to first test within the project, and validate that it really worked, it was all
///       pretty straight forward with implementation. I'm guessing that this was really the goal of the lab, 
///       to go through the though process and analyze, more than just writing out the code.
/// </summary>
class Program
{
    static void Main(string[] args)
    {
        Console.WriteLine("Hello, World!");
    }
}
