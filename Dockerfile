FROM frappe/erpnext:v15.0.0

# We need root to copy files into protected paths if needed, 
# but frappe user is standard.
USER root

# Create a customized directory for our Techxle scripts
RUN mkdir -p /home/frappe/frappe-bench/techxle

# Copy the scripts from the build context (GitHub Repo)
# matching the path where we pushed them (frappe/utils/...)
COPY frappe/utils/setup_*.py /home/frappe/frappe-bench/techxle/
COPY frappe/utils/cleanup_*.py /home/frappe/frappe-bench/techxle/
COPY frappe/utils/set_print_defaults.py /home/frappe/frappe-bench/techxle/

# Ensure permissions are correct
RUN chown -R frappe:frappe /home/frappe/frappe-bench/techxle

# Switch back to frappe user
USER frappe
