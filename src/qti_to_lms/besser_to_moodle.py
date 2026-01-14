import os
from jinja2 import Environment, FileSystemLoader
from src.qti_to_lms.metamodel.qti import TestDefinition


##############################
#    Moodle Generator
##############################
class MoodleGenerator():
    """Generate Moodle XML quiz format from Besser TestDefinition models.

    This class converts a TestDefinition domain model into a Moodle-compatible
    quiz structure using Jinja2 templating. It handles template rendering and
    output file generation.

    Attributes:
        test_def (TestDefinition): The test definition model to convert.
        output_dir (str): Directory where generated Moodle code will be saved.
        output_file_name (str): Name of the output file to generate.

    Args:
        test_def: A TestDefinition domain model instance to convert.
        output_dir: Optional output directory (defaults to './output').
        output_file_name: Optional output file name for the generated quiz.
    """

    def __init__(
        self,
        test_def: TestDefinition,
        output_dir: str = None,
        output_file_name: str = None,
    ):
        self.test_def = test_def
        self.output_dir = output_dir
        self.output_file_name = output_file_name


    def generate(self):
        """Generate Moodle quiz XML code and save it to the output file.

        Renders the test definition using the Jinja2 Moodle template and writes
        the generated code to the specified output file. Creates the output
        directory if it doesn't exist.

        The template used is 'moodle_template.py.j2' located in the templates
        directory alongside this module.

        Returns:
            None. Generates and writes output file as a side effect.

        Side Effects:
            - Creates output directory if it doesn't exist
            - Writes generated Moodle code to output file
            - Prints confirmation message with file path
        """

        # Ensure output_dir has a valid default
        if not self.output_dir:
            self.output_dir = os.path.join(os.getcwd(), "output")

        os.makedirs(self.output_dir, exist_ok=True)

        file_path = os.path.join(self.output_dir, self.output_file_name)
        generated_code = self._render_template()

        with open(file_path, mode="w", encoding="utf-8") as f:
            f.write(generated_code)
            print("✅ Moodle Code generated in the location: " + file_path)

    def _render_template(self) -> str:
        """Render the Moodle template with test definition data.

        Returns:
            The rendered template as a string.
        """
        templates_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "templates"
        )
        env = Environment(loader=FileSystemLoader(templates_path))
        template = env.get_template('moodle_template.py.j2')

        return template.render(
            output_file_name=self.output_file_name,
            test_def=self.test_def
        )

