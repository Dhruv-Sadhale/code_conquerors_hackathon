# Club Navigator — Flow Description and Test Case Guide

This document outlines the flow of the **Club Navigator** application and highlights key buttons, redirections, and user/admin interactions. Based on this, please use the attached document to fill in the possible **test cases** and their **expected results**.

---

## Home Page Navigation

The homepage consists of the following interactive buttons:

1. **Admin Google Login** → Redirects to the Google OAuth login for admins.
2. **User Google Login** → Redirects to the Google OAuth login for students/users.
3. **Club Carousel View** → Opens a public, scrollable carousel showcasing all clubs.
4. **Take Test** → Redirects to the psychometric test interface. *(Requires user login)*

---

## Admin Flow

Once an admin successfully logs in:

- Admin is redirected to a dashboard displaying links to **all clubs’ core pages**.
- By clicking any club’s dashboard link, the admin can:
  - **View applicants**.
  - **Induct students** into the club by transferring them from the applicant list to the inducted list.

---

## User Flow

Upon successful user login:

- The user is redirected to their **personal dashboard**, which includes:
  - A list of clubs they have already been **inducted into**, each linking to the club's core dashboard (shared with admins).
  - A section displaying **recommended clubs**, based on the user's most recent psychometric test attempt.

---

## Psychometric Test Flow

- Users can choose to **take the test** via the navigation bar.
- On clicking the test link:
  - A **Gemini API** call is made with a tailored prompt.
  - The user is presented with **10 personalized questions**, each with 4 options.
  - Questions are displayed one-by-one, and the next question appears **only after selecting an option**.

---

## Recommendation Generation

- After completing the test:
  - A **"Generate Recommendation List"** button appears.
  - Clicking it triggers another **Gemini API** call to predict the top **3 clubs** for the user.
  - Upon successful response:
    - User is redirected to the dashboard.
    - A new set of **3 recommended clubs** is displayed.
    - A confirmation **email** is sent to the user's login email confirming test completion and recommendations.

---

## User Satisfaction Flow

At the bottom of the user dashboard:

- **“Are you satisfied with the test results?”**
  - If **No**: A **feedback form** appears that the user can fill out and submit.
  - If **Yes**:
    - The user can click on any of the 3 recommended clubs to:
      - **Notify club admins**.
      - Express interest in becoming an **applicant** for the club's induction process.

---

## Next Steps

Based on the above functional flow, kindly fill out the attached test case document with:

- **Button / Action**
- **Expected Redirection / Behavior**
- **Preconditions**
- **Expected Result**
- **Actual Result (post-testing)**

---

Feel free to modify this document further based on project updates. Let’s ensure thorough testing for a smooth onboarding experience across all roles!


TEAM MEMBERS: 
1. Dhruv Sadhale
2. Apurva Gokhale
3. Arjun Deodhar
4. Deep Oak
