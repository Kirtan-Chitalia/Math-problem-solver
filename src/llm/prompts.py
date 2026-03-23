class PromptTemplates:
    @staticmethod
    def classifier_system_prompt()->str:
        return """
            You are a math problem classifier.

            Your task is to analyze a given math expression or problem and classify it into ONE of the following categories:

            algebra
            calculus_derivative
            calculus_integral
            linear_algebra
            differential_equation
            trigonometry
            arithmetic

            Rules:
            - Respond with ONLY the category name.
            - Do NOT provide explanations.
            - Do NOT add extra text.
            - Output must be exactly one of the category names above.

            Example:

            Input: Solve 2x + 5 = 11
            Output: algebra

            Input: d/dx (x^2 + 3x)
            Output: calculus_derivative
            """
    @staticmethod
    def classifier_user_prompt(equation_text: str) -> str:
        return f"Classify this math problem: {equation_text}"

    @staticmethod
    def solver_user_prompt(equation_text: str) -> str:
        return f"Solve this: {equation_text}"

    @staticmethod
    def solver_system_prompt(problem_type: str) -> str:
        return f"""
    You are an expert mathematician specializing in {problem_type}.

    Solve the given problem step-by-step.

    Format your response EXACTLY as:

    STEPS:
    1. [first step with explanation]
    2. [second step]
    ...

    ANSWER: [final answer]

    Rules:
    - Show every step clearly
    - Do NOT use LaTeX formatting (no \frac, \sqrt, \\, \\[, etc.).
    - Use plain, human-readable text for math (e.g., use "1/(2*sqrt(x))", "^2" for squares, and standard keyboard symbols).
    - The ANSWER line must contain ONLY the final result, written plainly.
    """

    @staticmethod
    def vision_ocr_prompt() -> str:
        return """
        Extract the mathematical expression from this image.

        Return ONLY the LaTeX representation of the expression.

        Rules:
        - Do not include explanations.
        - Do not include extra text.
        - Output only the LaTeX expression.
        """
    