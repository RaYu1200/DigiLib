import { Directive, EventEmitter, HostListener, Output } from '@angular/core';

@Directive({
  selector: '[drmDropFile]'
})
export class DropFileDirective {

  @Output() onFileDropped = new EventEmitter<any>();


  @HostListener("dragover", ["$event"]) public onDragOver(evt: DragEvent) {
    evt.preventDefault();
    evt.stopPropagation();
  }

  @HostListener("dragleave", ["$event"]) public onDragLeave(evt: DragEvent) {
    evt.preventDefault();
    evt.stopPropagation();
  }

  @HostListener('drop', ['$event']) public onDrop(evt : any): any {
    evt.preventDefault();
    evt.stopPropagation(); 
    const files = evt.dataTransfer.files;
    if (files.length > 0) {
      this.onFileDropped.emit(files);
    }
  }

}
