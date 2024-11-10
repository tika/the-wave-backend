### Install Dependencies

You can install the required Python dependencies using `pip` and the `requirements.txt` file.

1. Create a virtual environment (optional but recommended):

   ```bash
   python3 -m venv venv
   ```

2. Activate the virtual environment:

   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Setup MongoDB

#### **Option 1: Using Local MongoDB**

To use a local MongoDB instance, ensure you have MongoDB installed on your machine. You can follow the installation steps here: [MongoDB Installation Guide](https://www.mongodb.com/docs/manual/installation/).

Once MongoDB is installed, you can start it by running:

```bash
mongosh
```
