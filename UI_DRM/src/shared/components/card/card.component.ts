import { ChangeDetectorRef, Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'drm-card',
  templateUrl: './card.component.html',
  styleUrls: ['./card.component.scss'],
})
export class CardComponent implements OnInit {

  @Input() set fileName(name : string){

    if(name == undefined) return;
    this._fileName = name;
    this.type = name.split('.').pop();

  }

  
  type: string = "docs";

  _fileName : string= 'component.ts';

  @Input() url: string;
  @Input() keyWords: string;
  @Input() uploadedAt: string;


  constructor(private _cd : ChangeDetectorRef){}

  ngOnInit(): void {
  }

  download(){
    window.open(this.url, '_blank')
  }
}
