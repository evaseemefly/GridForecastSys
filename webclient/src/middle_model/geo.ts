class WMSOptionsMidModel {
  public layer: string
  public format: string
  public style?: string
  public transparent: boolean
  public zindex?: number

  constructor(
    layer: string,
    zindex = 1500,
    style?: string,
    format = 'image/png',
    trans = true
  ) {
    this.layer = layer
    this.format = format
    this.transparent = trans
    this.zindex = zindex
    this.style = style
  }
}

class WMSMidModel {
  public url: string
  public options: WMSOptionsMidModel

  constructor(url: string, options: WMSOptionsMidModel) {
    this.url = url
    this.options = options
  }
}

export { WMSMidModel, WMSOptionsMidModel }
