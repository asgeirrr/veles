use reqwest;
use std::env;
use reqwest::{Error};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use serde_this_or_that::as_string;


#[derive(Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
struct FioResponse {
    account_statement: AccountStatement,
}


#[derive(Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
struct AccountStatement {
    info: AccountInfo,
    transaction_list: TransactionList,
}

#[derive(Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
struct AccountInfo {
    account_id: String,
    bank_id: String,
    iban: String,
    bic: String,
    opening_balance: f64,
    closing_balance: f64,
    date_start: String,
    date_end: String,
    year_list: Option<String>,
    id_list: Option<i64>,
    id_from: Option<i64>,
    id_to: Option<i64>,
    id_last_download: Option<i64>,
}

#[derive(Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
struct TransactionList {
    transaction: Vec<HashMap<String, Option<RawValue>>>,
}


#[derive(Serialize, Deserialize, Debug)]
#[serde(rename_all = "camelCase")]
pub struct RawValue {
    id: u64,
    name: String,
    #[serde(deserialize_with = "as_string")]
    value: String,
}

pub fn download_transactions() -> Result<String, Error>{
    let token = env::var("FIO_TOKEN").unwrap();
    let url = format!("https://www.fio.cz/ib_api/rest/periods/{token}/{date_from}/{date_to}/transactions.json", token=token, date_from="2023-8-1", date_to="2023-9-1");
    let response = reqwest::blocking::get(&url)?;
    println!("Fetched transaction list from Fio with HTTP {}", response.status());
    let text = response.text()?;
    return Ok(text)
}


pub fn parse_transactions(text: String) -> Vec<HashMap<String, Option<RawValue>>>{
    let deserialized: FioResponse= serde_json::from_str(&text).unwrap();
    let raw_transactions = deserialized.account_statement.transaction_list.transaction;
    println!("Parsed {} transactions", raw_transactions.len());
    return raw_transactions
}
