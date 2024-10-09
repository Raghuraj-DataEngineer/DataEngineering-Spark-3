{
 "cells": [
  {
   "attachments": {},
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Dummy Data Generator\n",
    "> More at [the official Faker Docs website](https://zetcode.com/python/faker/)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Install libraries:\n",
    "```bash\n",
    "source venv/bin/activate\n",
    "pip install pyspark Faker pandas\n",
    "```"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import random\n",
    "import string\n",
    "from pyspark.sql import SparkSession\n",
    "from time import sleep\n",
    "from faker import Faker\n",
    "\n",
    "faker = Faker()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "def generate_fake_iot(num=1):\n",
    "    # Fake devices\n",
    "    devices_list = ['device_1','device_2','device_3','device_4']\n",
    "\n",
    "    # Schema\n",
    "    output = [{\"device_id\":random.choice(devices_list),\n",
    "                   \"device_model_id\":''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(2)),\n",
    "                   \"building_area_id\":faker.city(),\n",
    "                   \"ts\":pd.Timestamp(pd.Timestamp.now(), unit='ms')\n",
    "                } for x in range(num)]\n",
    "    return output\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Note!\n",
    "If you want to see the Live demo, to aggregate data in real time, run the following in terminal and then run the next cell:\n",
    "\n",
    "```\n",
    "spark-submit spark-streaming-demo-2.py \n",
    "```"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [],
   "source": [
    "# See data\n",
    "for i in range(5):\n",
    "    df_iot = pd.DataFrame(generate_fake_iot(100))\n",
    "    df_iot.to_csv(f\"../spark_jobs/datasets/file_{i}.csv\", encoding='utf-8', index=False, header=True)\n",
    "    sleep(5)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### While this is running, go to the terminal where you're running the spark-streaming-demo-2 app"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "venv",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.6"
  },
  "orig_nbformat": 4
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
