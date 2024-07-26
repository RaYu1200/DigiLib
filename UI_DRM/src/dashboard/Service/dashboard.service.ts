import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";


const root = 'http://localhost:8000';

const api  = {
    PUT_RECORD : '/api/upload',
    GET_RECORDS : '/api/search'
}


export interface IRecords    {

    metaData : {
        Items : IItems[]    
    }

}

export interface IItems{
    fileName : IfileName,
    uploadedAt : IUploadedAt,
    s3Url : IS3URL,
    keyWords : IKeywords
}

export interface IUploadedAt {
    S : string
}

export interface IfileName{
    S : string
}

export interface IS3URL {
    S : string
}

export interface IPaload {
    file : string,
    uploadedAt : string,
    keywords : string[]
}

export interface IKeywords{
    S : string;
}


@Injectable({
    providedIn: 'root'
  })
  
  export class DashaboarService {
  
    constructor(private client: HttpClient) {



    }  

    getRecords( Params){

        console.log("in service");
        console.log(Params)
        return this.client.get<IRecords>(root + api.GET_RECORDS, {params: Params} );
    }

    putRecords(payload : any){
        return this.client.post(root + api.PUT_RECORD,payload);
    }

}