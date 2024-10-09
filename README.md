# Bored Ape Listener
A simple app for listening and recording transfer events for the Bored Ape Yacht Club (BAYC) NFTs, in the Ethereum blockchain.

## 1. Pre-Installation
Before installation, make sure to have done the following:

### 1.1. Virtual Environment Set-up
We will run the app in a virtual environment. Make sure to create your environment (anywhere you like except the project root), then activate it. In my case, I would like to name it `bored-ape-venv`, but you can use anything you like.

**Linux**
```
$ py -m venv bored-ape-venv
$ source bored-ape-venv/bin/activate
```

**Windows**
```
 > py -m venv bayc-venv
 > "bayc-venv/Scripts/activate"
```

### 1.2. .env Set-up
Create a .env file inside the project root, with the following contents:
```
INFURA_URL_ETH_MAINNET=""
BAYC_CONTRACT_ADDRESS="0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d"
```

We will supply the correct values for the `INFURA_URL_ETH_MAINNET` variable in a while.

### 1.3. Infura Account Set-up
The app uses Infura to connect to the Ethereum Mainnet. Do the following if you have not set up an account yet.

##### 1.3.1. Account set up
[Signup](https://app.infura.io/register) for an Infura account.

##### 1.3.2. Once registered, head over to the Dashboard.
You will have your default API key `My First Key`. You may create a new one, but the default should suffice for this project.

![image](https://img001.prntscr.com/file/img001/QkPYrSW4Q1OdE_KrSLFLtA.png "Default API Keys")

##### 1.3.3. Enable mainnet
You got to make sure that the Ethereum Mainnet is enabled. To do this, configure `My First Key`, then go to **All Endpoints** section.

![image](https://img001.prntscr.com/file/img001/N2YukhEATS6U-r4pneEbgg.png "Ethereum Mainnet enabled")

##### 1.3.4. Get RPC URL
Finally, go to the **Active Endpoints** section, copy the RPC URL for Ethereum Mainnet, then supply it as the value for `INFURA_URL_ETH_MAINNET` env variable.

![image](https://img001.prntscr.com/file/img001/EzkklOzIRW6vXVw7v2HJhg.png "Ethereum Mainnet enabled")

Your `.env` file should now look like this:
```
INFURA_URL_ETH_MAINNET="https://mainnet.infura.io/v3/e3df95b4c2a34838acd34e0f4de0756c"
BAYC_CONTRACT_ADDRESS="0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d"
```

Thats it! Your Infura account and environment variables are now setup.

## 2. Python Dependencies

- Django 5.1.1
- Django REST Framework 3.15.2
- python-decouple 3.8
- web3 7.3.0

With the virtual environment enabled, install these dependecies via the following command:

```
pip install -r requirements.txt
```

> INFORMATION:
>
> We use `djangorestframework` library in order to easily perform data serialization. In most of my Django projects, this is one of the must-have for me.
>
> We also use `python-decouple` because we aim to save data that may eventually change. In order to avoid updating the code when these data change, we use .env to store them. And we use the library to retrieve those values easily within the code.
>

## 3. Database Migration

Next thing to do is to build up our `transfer` table, which we defined via the Transfer model defined in `./events/models.py`.

Firs, create an sqlite3 file within the project root.

```
mkdir db.sqlite3
```

Next, create the migration file using the `makemigrations` command, specifying the `events` module

```
python manage.py makemigrations events
```

The above command will have the following output:
```
Migrations for 'events':
  events\migrations\0001_initial.py
    + Create model Transfer
```

Finally, perform the actual migration with the `migrate` command

```
python manage.py migrate events
```
The above command is successfull if you see the following output:
```
Operations to perform:
  Apply all migrations: events
Running migrations:
  Applying events.0001_initial... OK
```

## 4. The ABI
We use a very simple ABI for this app, with only the `Transfer` event defined in it. The ABI file is located at `./core/abis/TransferABI.json`
```
{
    "abi": [{
        "anonymous": false,
        "inputs": [{
            "indexed": true,
            "internalType": "address",
            "name": "from",
            "type": "address"
        }, {
            "indexed": true,
            "internalType": "address",
            "name": "to",
            "type": "address"
        }, {
            "indexed": true,
            "internalType": "uint256",
            "name": "tokenId",
            "type": "uint256"
        }],
        "name": "Transfer",
        "type": "event"
    }]
}
```

## 5. Testing

There are 2 phases of the app.

1. A script that we run to listen and record transfer events based on a given block range
2. An exposed `GET` endpoint for retrieving transfer history based on a given token ID.

### 5.1 Listening and Recording

Inside the project root, there is a file called `./bored-ape.py`. Run this via the terminal to begin listening and recording transfer events.

There are 2 arguments for the script:
- start (required) - specifies at which block to start the listening to
- end (optional) - specifies at which block to end the listen to; defaults to 'latest'.

```
python bored-ape.py --start=20925805
```

A sample output will look something like this:
```
Web3 connection established!
Transfer event for token 6473 with transaction hash 700317ddf2eec33bb67335b9897917eb9c558c000935e360800e7304f83a3bbd has been recorded successfully.
Transfer event for token 5809 with transaction hash b5c91ab05299e7966c931c412ab3542c09f9c559cb35b80d529da8a83e240653 has been recorded successfully.
Transfer event for token 7940 with transaction hash 7fbb3ffdae4441dec541422d9810700e63bfbff78b411dca85fb6f070068bcca has been recorded successfully.
Transfer event for token 6828 with transaction hash b80787977d825a5a95c228f4ada1e62b50e180fab3b2b7e414d458ea6ba6b8aa has been recorded successfully.
Transfer event for token 6828 with transaction hash 55cdef0d7daa601063d21feeafd5566b9fc7d2e2ef2f61858ddfb4d4d135efa6 has been recorded successfully.
```

### 5.2 Fetching Transfer History

To fetch the transfer history of a token ID, first start the Django server:

```
python manage.py runserver
```

On your browser, head over to `http://localhost:8000/api/events/transfers/<token_id>/`. Replace the `<token_id>` with the actual token ID that you want to fetch for.

A sample output looks something like this:
```
{
    "success": true,
    "message": "Fetch success",
    "data": [
        {
            "id": 9,
            "token_id": "6828",
            "sender": "0x020cA66C30beC2c4Fe3861a94E4DB4A498A35872",
            "recipient": "0x1EA27bCE786a81022dFc156059771e8d3279a9a6",
            "trn_hash": "b80787977d825a5a95c228f4ada1e62b50e180fab3b2b7e414d458ea6ba6b8aa",
            "block_no": 20926163
        },
        {
            "id": 10,
            "token_id": "6828",
            "sender": "0x1EA27bCE786a81022dFc156059771e8d3279a9a6",
            "recipient": "0x29469395eAf6f95920E59F858042f0e28D98a20B",
            "trn_hash": "55cdef0d7daa601063d21feeafd5566b9fc7d2e2ef2f61858ddfb4d4d135efa6",
            "block_no": 20926172
        }
    ]
}
```

### And there you go! You have successfully ran the app at this point.