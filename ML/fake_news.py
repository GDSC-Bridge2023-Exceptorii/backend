from transformers import AutoModelForSequenceClassification, AutoTokenizer

access_token: str = "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"
model: AutoModelForSequenceClassification = AutoModelForSequenceClassification.from_pretrained("irfanns/autotrain-classification-3426893569", use_auth_token=access_token)

tokenizer: AutoTokenizer = AutoTokenizer.from_pretrained("irfanns/autotrain-classification-3426893569", use_auth_token=access_token)

def classify(text: str) -> str:
    """Classify news summaries using ML: Huggingface BERT."""
    inputs: AutoTokenizer = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)
    logits = outputs.logits
    prediction = logits.argmax()
    if prediction == 0:
        return "Real"
    elif prediction == 1:
        return "Fake"


if __name__ == "__main__":
    test_1 = "The advancement of AI is too fast and we need to be careful."
    test_2 = "Hackathons are fun: here's five reasons why."
    test_3 = "The new iPhone 12 is out and it's the best phone ever."
    test_4 = "Scammers are using the pandemic to steal your money."

#     test_5 = '''On March 23, 2010, President Barack Obama signed the Patient Protection and Affordable Care Act, the 906-page health care reform law known as Obamacare. It was, as a live microphone caught Vice President Joe Biden exclaiming to his boss, a big deal, with Biden memorably inserting an extra word for emphasis—and for history—between “big” and “deal.”

# Obamacare would cover millions of the uninsured, a giant step toward the Democratic dream of health care for all. It also included dozens of less prominent provisions to rein in the soaring cost and transform the dysfunctional delivery of American medicine. It was the kind of BFD that the most consequential presidencies are made of, even though it had squeaked through Congress without any Republican votes, and few Americans truly understood what was in it.

# Even fewer Americans understood what was in the Health Care and Education Reconciliation Act, the 55-page addendum that officially finalized Obamacare. This was the strange legislative vehicle that Democrats had jerry-rigged to drag reform around a Republican filibuster. Its substance was mostly an afterthought—the New York Times ran a dutiful story on page A16 after it passed—but as Obama noted when he signed it the next week at Northern Virginia Community College, it included another BFD.

# “What’s gotten overlooked amid all the hoopla, all the drama of last week, is what’s happened in education,” he said.

# Yes, education. Tucked into the parliamentary maneuver that rescued his health care law was a similarly radical reform of the trillion-dollar student loan program. When Biden’s wife, Jill, a professor at Northern Virginia, introduced Obama that day, she called it “another historic piece of legislation.” The House Republican leader, John Boehner of Ohio, complained that “today, the president will sign not one, but two job-killing government takeovers.”

# Obamacare wasn’t really a government takeover, but the student loan overhaul actually was; it yanked the program away from Sallie Mae and other private lenders that had raked in enormous fees without taking much risk. The bill then diverted the budget savings into a $36 billion expansion of Pell Grants for low-income undergraduates, plus an unheralded but extraordinary student-debt relief effort that is now quietly transferring the burden of college loans from struggling borrowers to taxpayers. It all added up to a revolution in how America finances higher education, completely overshadowed by the health care hoopla and drama.

# Over the past seven years, Americans have heard an awful lot about Barack Obama and his presidency, but the actual substance of his domestic policies and their impact on the country remain poorly understood. He has engineered quite a few quiet revolutions—and some of his louder revolutions are shaking up the status quo in quiet ways. Obama is often dinged for failing to deliver on the hope-and-change rhetoric that inspired so many voters during his ascent to the presidency. But a review of his record shows that the Obama era has produced much more sweeping change than most of his supporters or detractors realize.

# It’s true that Obama failed to create the post-partisan political change he originally promised during his yes-we-can pursuit of the White House. Washington remains as hyperpartisan and broken as ever. But he also promised dramatic policy change, vowing to reinvent America’s approach to issues like health care, education, energy, climate and finance, and that promise he has kept. When you add up all the legislation from his frenetic first two years, when Democrats controlled Congress, and all the methodical executive actions from the past five years, after Republicans blocked his legislative path, this has been a BFD of a presidency, a profound course correction engineered by relentless government activism. As a candidate, Obama was often dismissed as a talker, a silver-tongued political savant with no real record of achievement. But ever since he took office during a raging economic crisis, he’s turned out to be much more of a doer, an action-oriented policy grind who has often failed to communicate what he’s done.

# What he’s done is changing the way we produce and consume energy, the way doctors and hospitals treat us, the academic standards in our schools and the long-term fiscal trajectory of the nation. Gays can now serve openly in the military, insurers can no longer deny coverage because of pre-existing conditions, credit card companies can no longer impose hidden fees and markets no longer believe the biggest banks are too big to fail. Solar energy installations are up nearly 2,000 percent, and carbon emissions have dropped even though the economy is growing. Even Republicans like Ted Cruz and Marco Rubio, who hope to succeed Obama and undo his achievements, have been complaining on the campaign trail that he’s accomplished most of his agenda.

# “The change is real,” says Ron Klain, who served as Biden’s White House chief of staff, and later as Obama’s Ebola czar. “It would be nice if more people understood the change.”

# In a conflict-obsessed media environment that is not exactly geared toward substantive policy analysis, Obama’s technocratic brand of change has tended to be more opaque than, say, Donald Trump’s plan for a wall along the Mexican border or Bernie Sanders’ promise of free college for all. At times, its complexity has camouflaged its ambition. At other times, its ambition hasn’t lived up to Obama’s rhetoric; not everything has changed in the Obama era. For example, he talked a big game about eliminating wasteful programs, but other than killing the F-22 fighter jet, an absurdly expensive presidential helicopter and a hopelessly captured bank regulatory agency called the Office of Thrift Supervision, he hasn’t done much of that.

# The most obvious thing Obama hasn’t done is usher in a new era of public enthusiasm for government action and the Democratic Party. He was reelected by a comfortable margin, but conservative Republicans have taken back both houses of Congress and made impressive gains in statehouses on his watch, riding a powerful wave of hostility to federal overreach. That political legacy could imperil some of Obama’s left-of-center policy legacy if a Republican is elected to succeed him. It has already stymied gun control and immigration reform, while forcing Obama to accept deep spending cuts he didn’t want.

# But it’s remarkable how often Obama has gotten what he wanted, in many cases policies that Democrats (and sometimes moderate Republicans) have wanted for decades, and how often those policies have slipped under the radar.

# '''
    print(classify(test_1))
    print(classify(test_2))
    print(classify(test_3))
    print(classify(test_4))
    # print(classify(test_5))