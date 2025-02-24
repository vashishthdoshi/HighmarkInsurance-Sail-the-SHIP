"""
@author: Vashishth Doshi | vbd@andrew.cmu.edu |vashishth.doshi@gmail.com
Python Programming II - Project Deliverable - Under instructor Dr. Barrett - For Team Py-neers Part 3 of Project | Documentation, User Instruction and Abstract in accompanying files.
"""

#libraries used = beautifulSoup, requests, re to assist wth coding functionality. BeautifulSoup helps with parsing html, requests helps request html from webpages and re helps in pattern-matching in strings.
from bs4 import BeautifulSoup
import requests
import re

#web scraping insurance terminology data from CMS.gov
url = "https://www.cms.gov/medical-bill-rights/help/guides/health-insurance-terms"
common_questions_page = requests.get(url)
soup = BeautifulSoup(common_questions_page.text, "html.parser")
#print(beautifulSoup) - print have been hashtagged for future use as checkpoints.
terms = []
meanings = []

h3_tags = soup.find_all('h3')
for h3 in h3_tags:
    terms.append(h3.text.strip())
#print(terms)
#print(len(terms)) - checks original length of scraped list

p_tags = soup.find_all('p')
for p in p_tags:
    text = p.text.strip()
    if text:
        meanings.append(text)
meanings = [m for m in meanings if m]
#print(meanings)
#print(len(meanings))

if len(terms) > 21:
    terms = terms[37:-1]
if len(meanings) > 28:
    meanings = meanings[5:-5]

meanings[0] = ' '.join(meanings[0:3])
meanings[3] = ' '.join(meanings[3:5])
meanings[5] = ' '.join(meanings[5:7])
meanings[8] = ' '.join(meanings[8:10])
meanings[11] = ' '.join(meanings[11:13])
meanings[20] = ' '.join(meanings[20:22])

new_meanings = [meanings[i] for i in [0, 3, 5, 7, 8, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20]]
new_meanings.extend(meanings[22:])
#print(new_meanings) after data cleaning and joining some seperate strings due to paragraphing on webpage.
#print(len(new_meanings)) #should be 21 - one for each term.
#print(terms)
#print(len(terms)) - should be 21

# dictionary of questions and answers from CMU SHIP website - https://www.cmu.edu/health-services/student-insurance/faqs.html
programvd_structure = {
    "A": {
        "1": ["Contacts for questions about SHIP enrolment or waiver status", 
              "HUB International: Phone Number: 888-777-9980\nEmail: CMUSHIP@hubinternational.com\nCMU Student Health Insurance Phone Number: 412-268-2157 option 3\nEmail: shinsure@andrew.cmu.edu"],
        "2": ["Contacts for questions about SHIP coverage (medical procedures, medication, etc.)", 
              "Refer to SHIP Plan Documents\nCall the Highmark number on the back of your insurance card or email UHS."],
        "3": ["Contacts for questions about insurance charges on your student account", 
              "CMU Student Health Insurance Phone Number: 412-268-2157 option 3\nEmail: shinsure@andrew.cmu.edu"],
        "4": ["Contacts for questions to update your name, gender, birthdate or mailing address with Highmark", 
              "HUB International Email: cmuship@hubinternational.com"]
    },
    "B": {
        "1": ["Does my insurance enrollment or waiver carry over each year or do I need to re-apply", 
              "Enrollments and waivers do not carry over from one year to the next; completing Open Enrollment is an annual requirement. Students must enroll in or waive the CMU SHIP every academic year that they are enrolled at the university."],
        "2": ["There is a charge for insurance on my student account, but I did not enroll in the CMU SHIP", 
              "At the start of each academic year, all students enrolled in degree-seeking programs are assessed a default fee for the CMU Student Health Insurance Plan (SHIP). This is a placeholder fee until Open Enrollment is completed. Open Enrollment is the annual period in which students must either enroll in or apply to waive the CMU SHIP.\n\nIf you do not complete Open Enrollment, you will be auto-enrolled in the CMU SHIP and the insurance fee will remain on your student account.\n\nIf you receive an approved waiver, the insurance fee will be credited back to your student account.\n\nPlease note that invoices do not update, as they are statements that reflect a point in time. Please check the Account Activity section in SIO for up-to-date charges and credits.\n\nStudent account or invoice questions should be directed to Student Financial Services."],
        "3": ["I paid the insurance fee in my student account. Am I enrolled in the SHIP?", 
              "No, paying the student insurance fee does not complete your insurance enrollment. In order to enroll during Open Enrollment, students must:\n1. Log into SIO, go to Campus Life, then Health Insurance.\n2. Click any of the Highmark links to access the insurance portal.\n3. Follow the instructions to enroll.\n4. Click CONFIRM to submit your enrollment."],
        "4": ["I need my insurance ID card. Where can I find my insurance information?", 
              "Insurance ID cards should arrive 2-3 weeks after your enrollment has been processed. If your card did not arrive:\n\nCheck the mailing address attached to your insurance enrollment. If it has changed or was incomplete, you will need to update it. You can update your address through the insurance portal in SIO or email your new, complete address (street address, apartment or SMC, city, state and zip code) to HUB International (Email: CMUSHIP@hubinternational.com)\n\nCheck your insurance portal in SIO for your insurance member ID number. Use your member ID to register an account at highmarkbcbs.com. There, you can access a digital insurance card and order new cards\n\nIf you are still having difficulty, contact HUB International at Phone Number: 888-777-9980 or Email: cmuship@hubinternational.com"],
        "5": ["I do not have a U.S. mailing address yet. Can I enroll in the SHIP?", 
              "A U.S. mailing address is required to enroll in the CMU SHIP. Enrollments submitted with a non-U.S. address or an incomplete address will not be processed.\n\nInternational students enrolling in the CMU SHIP should wait until they have secured a U.S. mailing address where they can receive mail before submitting an enrollment. Waiting until later in the Open Enrollment period to enroll in the SHIP will not affect the coverage dates. SHIP coverage begins on August 1 each academic year, even if you do not submit your enrollment until the end of the open enrollment period"],
        "6": ["If I am graduating in December, can I enroll in the SHIP for August - December only? Can I enroll only for the months I am on campus?", 
              "The CMU SHIP is a full year plan with a coverage period of August 1 - July 31 each academic year. Students entering CMU in the Fall are enrolled and charged for the full coverage year.\n\nStudents graduating in December can request to cancel the SHIP at that time; it does not cancel automatically. Students with an approved cancellation will receive a prorated refund of the remaining months' premiums on the medical, dental and/or vision plans (with adjustment for any PhD student insurance support, if applicable). SHIP cancellations are effective from the first of the month following the month in which the cancellation form is received. Cancellations are not permitted after March 31.\n\nIf you are graduating in December and would like to cancel your insurance plan, please Email shinsure@andrew.cmu.edu for assistance."],
        "7": ["I am a PhD student graduating in August. Can I enroll in the SHIP for only the month of August?", 
              "Yes. Students graduating in August are eligible to enroll in the medical SHIP for the month of August only. August-only enrollments are only available for the student medical plan; dental and vision plans are not available.\n\nAugust-only enrollments can be completed by emailing shinsure@andrew.cmu.edu for assistance."],
        "8": ["Outside of Open Enrollment, can I enroll in the medical, dental or vision plans? What if I want to add or remove someone from my plan?", 
              "You can only enroll outside of your Open Enrollment period if you have had a qualifying event (for example, involuntary loss of insurance, including due to turning age 26 – check healthcare.gov/glossary/qualifying-life-event). This applies to the student medical, dental and vision plans; you cannot add the dental or vision plan outside of Open Enrollment without a qualifying event.\n\nIf you are enrolled in a plan, you can also add dependents who have had a qualifying event (for example, birth/adoption of a child or arrival to the U.S. for the first time during the coverage year).\n\nFor qualifying event enrollments into the medical, dental or vision plans, you have 90 days from the event to enroll and will need to provide supporting documentation.\n\nRemoving Dependents:\nDependents can be removed from your insurance plan at any time before March 31 of the coverage year.\nTo make any of these changes, please email shinsure@andrew.cmu.edu for assistance."],
        "9": ["How do I find in-network health care providers? What if I need to see a doctor or fill a prescription while I am away from campus?", 
              "The CMU SHIP is a national plan, with participating in-network providers in every state. Search for medical care, dental care, vision care and pharmacies in your desired location on the Highmark portal.\n\nFor Medical Care:\n1. Log in/register (you can do this using your member ID card).\n2. Select Find Doctors and Rx.\n3. Select Find a Doctor or Hospital / Find a Vision Care Provider / Find a Dentist.\n4. For medical services, enter BCBS PPO under the Network Tab.\n5. Enter location.\n6. Select the category of care.\nAlways be sure to confirm directly with the health care provider or facility that they are a participating provider in the CMU SHIP.\n\nFor Prescriptions:\n1. Log in/register (you can do this using your member ID card).\n2. Select Find Doctors and Rx.\n3. Go to Find a Pharmacy and select National Plus Network Pharmacy\n4. If you are living or traveling abroad, the CMU SHIP medical plan also provides members with a global network of healthcare providers through BCBS Global Core (https://www.cmu.edu/health-services/student-insurance/pdfs/global-core-travel-living-abroad.pdf), along with 24 hour emergency medical and travel assistance through the AXA Travel Assistance Program (https://www.cmu.edu/health-services/student-insurance/pdfs/axa-travel-assistance.pdf)."],
        "10": ["Why did Highmark send me a letter asking for my Social Security or Tax ID number?", 
               "CMU is not using Social Security Numbers for student insurance enrollment, but Highmark is required by law to send letters on an annual basis to members requesting their Social Security/Tax Identification Number. Members who do not provide this information will not be penalized, nor are they required to provide the information. Students may disregard the letter."],
        "11": ["Can I extend the SHIP after graduating in May?", 
               "After graduating in May, students are no longer eligible to enroll in or extend the SHIP. The SHIP coverage ends on July 31 of each academic year.\n\nCOBRA is offered with employer-based plans; there is no COBRA option for the student insurance plan.\n\nStudents graduating in August are eligible to enroll in the SHIP for the month of August only. August-only enrollments can be completed by emailing shinsure@andrew.cmu.edu for assistance."],
        "12": ["I no longer want my student insurance plan/s. Can I cancel the SHIP?", 
               "Cancellations are only available under the following circumstances:\n-December Graduation (or September certification for doctoral students graduating in December)\n-Formal separation from CMU (i.e. leave of absence, withdrawal, suspension, forfeit)\n-Fall semester foreign exchange students returning to their university after the fall semester\n-Enrollment in Medicaid in the state in which you are studying (e.g., a Pittsburgh campus student approved for enrollment into PA Medicaid). Enrollment is based on eligibility and the application process can be lengthy. Students must also have applied for Medicaid before or during their open enrollment period.\n\nThe option to join a new plan does not make a student eligible to cancel their current insurance enrollment.\n\nIf you meet the last criterion, email UHS (shinsure@andrew.cmu.edu) when your university enrollment status has been updated to reflect one of the statuses listed above (or when you wish to remove a dependent or have been approved for Medicaid) and we can assist you. You may be eligible to receive a pro-rated refund for the remaining months' premiums. The final deadline to submit a cancellation request form is March 31 and the insurance plan cannot be canceled after April 1 (May, June and July cancellations are not permitted)."],
        "13": ["Medical bill related questions", 
               "Depending on the treatment you received, you may have a co-pay or an amount not covered by your insurance plan. The bill from the medical provider will show the charges for the treatment, what your insurance plan has paid and what you may owe. If you have questions about the amount owed, the first step is to consult your Explanation of Benefits (EOB), which you can find in the claims sections of your Highmark portal. The EOB will describe what your insurance plan paid to the provider on your behalf.\n\nIf the bill does not show that insurance was applied to your bill, please contact the medical provider directly and give them your insurance information.\n\nIf you have questions about what was covered by your insurance, you can call the member services phone number on your insurance card.\n\nFor questions about medical bills or charges:\n- From an off-campus health care provider, contact the provider directly.\n- From University Health Services, call 412-268-2157 option 2 or email the UHS team.\n- For itemized statements from UHS, log into HealthConnect and select statements/receipts from the menu."],
        "14": ["Insurance related terms", 
               "Understanding an insurance plan can be confusing, so it is important to understand your plan’s benefits and coverage. To understand the SHIP, we recommend you review the plan’s Summary of Benefits and Coverage.\n\nProduced by the University of Michigan, this informative video (https://uhs.umich.edu/insurance-101-video) provides the basics about health insurance.\n\nYou can also Use the HealthCare.gov glossary (https://www.healthcare.gov/glossary/)  to understand MORE key terms.\n\nBeing familiar with the following terms will also be helpful:\n\nIn-Network and Out-of-Network: In-Network providers (doctors) or facilities (laboratories, urgent care centers, hospitals, or imaging centers) participate in your insurance plan network. The most cost effective way to seek care is to see healthcare providers that are in-network. If you have the CMU SHIP and see an in-network provider, there is no deductible. \nOut-of-Network providers do not participate in your insurance plan network. If you have the CMU medical SHIP and see an out-of-network provider, the plan will cover 80% of the cost of the service after you meet your deductible. The dental plan has different coinsurance rates.\n\nCopays: Copays are a one-time payment at the time of service and can range depending on the service being provided. For the CMU SHIP, most copays are $0-$25. Some services have a higher copay, such as advanced imaging ($40), emergency room visits ($125), and hospital admissions ($150). You must pay the copay once for each visit where it is applicable. Prescriptions also incur a copay, but copays depend on the type of medication and frequency of refill.\n\nDeductible: A deductible is the amount of money you pay for health care services before your insurance plan starts to pay covered expenses. It is important to review insurance plans so you are aware if there is a deductible or not. Once the deductible is met, the plan will start covering benefits as outlined in the policy. The CMU medical SHIP has no deductible for in-network care, but there is a deductible for out-of-network care. The dental SHIP has a deductible for both in-network and out-of-network care.\n\nCoinsurance: Coinsurance is a portion of healthcare charges that the member is responsible to pay, usually after a deductible has been met. There is no coinsurance for in-network care with the CMU medical SHIP. For out-of-network care with the CMU SHIP, you would be responsible for 20% of covered charges, after paying the deductible amount. Coinsurance rates vary depending on the plan and the service, so you must review plan(s) carefully.\n\nExplanation of Benefits (EOB): EOBs show the total charges for your visit and which portion of charges the health insurance plan will cover. EOBs are not bills. EOBs help you understand how much your health plan covers, and what you can expect to pay when you get a bill from your provider."]
    
    },
    "C": {
        "1": ["Search health insurance terms and their explanations", ""]
    }
}

##base code ends
##program code starts. It contains the main while loop which circulates the user betwee three sections of the code, or allows them to quit. It contains the section C code which asks the user for input on the term they want the meaning of - and matches the input with scraped terms and returns corresponding meanings. It contains the section A and B loops which uses programvd_structure to output contacts/ answers corresponding to the user's chosen contacts/ questions they require.
print("Welcome to the CMU SHIP Question Section! We hope to help and answer all questions you may have")
print()
print("Section A is Quick Contacts related to CMU SHIP ")
print("Section B is Common Questions")
print("Section C is Health Insurance Term Search")

while True:
#while loop to toggle between sections A, B, C or quit.
    main_choice = input("\nEnter the section you want to explore (A, B, C) or 'quit' to exit: ").upper()
    
    if main_choice == 'QUIT':
        print("\nThank you for using the program! We hope it helped answer your questions :) ")
        break 
#breaks code when Quit is entered.

    if main_choice not in programvd_structure:
        print("\nError: Invalid choice. Please choose A or B or Q to quit.")
        continue 
#checking for errors, output prompts user to input valid terms
    
    if main_choice in programvd_structure: 
#if choice is in dict programvd_structure then runs

        if main_choice == 'C':
            while True:
                user_input = input("Enter a term (or part of a term) you want to know the meaning of (or enter 'back' to return to main menu): ").lower()
#runs for choice c, asks user for term they want to know the meaning of
                
                if user_input == 'back':
                    break
#if back is pressed code goes back to main_choice
                
                found_match = False 
                for i, term in enumerate(terms):
                    if re.search(r'\b\w*' + re.escape(user_input) + r'\w*\b', term.lower()):
                        print(f"\nTerm: {term}")
                        print(f"\nMeaning: {new_meanings[i]}")
                        print()
                        found_match = True
#for every [term] item, checks for input to match. if there is a match, found_match is true
                
                if not found_match: 
                    print("\nNo matching terms found. Remember to input terms without dash (-) characters/ and incorrect spacing.")
                print()
#if still not found match, output prompts user for better input with suggested error reasons.

        else:  
            current = programvd_structure[main_choice]
            print(f"\nYou chose {main_choice}. Please chose what question you have:")
            for key, value in current.items():
                print(f"{key}: {value[0]}")
                print()
#program if user choses section A or B. #prints every question with index.

            while True:
                question_num = input("\nChoose a question number (or 'b' to go back, 'q' to quit): ")
#prompts user to input the choice index of question.
                
                if question_num.lower() == 'q': 
                    print("\nThank you for using the quiz! We hope it helped answer your questions :) ")
                    exit()
#run if user choses q for quit.
                
                if question_num.lower() == 'b':
                    break
#run if user choses b to go back to main_choice

                if not question_num.isdigit():
                    print("\nError: Please enter a valid number between 1 and 14")
                    continue
#checks for invalid inpts which are not digits

                if question_num not in current:

                    print(f"Error: Question {question_num} does not exist. Please choose a valid question number.")
                    continue
                print()
                print(f"\nQuestion: {current[question_num][0]}")
                print(f"\nAnswer: \n{current[question_num][1]}")
#if question number not part of the list, then prints output asking for question from the given option. #prints chosen question and answer matching the index number to the corresponding question and answer.

                while True:
                    continue_choice = input("\nDo you want to choose another question from this section? (y/n): ").lower()
                    if continue_choice in ['y', 'n']:
                        break
                    print("\nError: Please enter 'y' for yes or 'n' for no.")
#prints choice of y to continue in section or n to leave for main_choice. #if input is not y or n, error is printed asking for only between y or n.

                if continue_choice == 'n':
                    break
#code breaks to main_choice if n is chosen
                
        pass
    else:
        print("Invalid section. Please choose A, B, or C.")
    print()
#prints invalid input for all other possible errors if user doesn't input correctly for A, B, C or quit. 

print("\nProgram ended")
#program ends - end of entire program :)